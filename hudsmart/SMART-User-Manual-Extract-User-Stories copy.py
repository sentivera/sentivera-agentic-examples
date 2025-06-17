#!/usr/bin/env python3
"""
extract_user_stories.py
---------------------------------
Process multiple User Handbook parts to extract user stories & features into a single CSV.

USAGE
    python extract_user_stories.py [number_of_files_to_process]

ENV
    OPENAI_API_KEY   (required, can be set in .env file)
"""

import os, sys, re, csv, textwrap, json, time
from pathlib import Path
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv

# ---------- CONFIG -----------------------------------------------------------------

MODEL                 = "o3"     # OpenAI model name
PAUSE_BETWEEN_CALLS   = 1.2     # polite delay to avoid rate limits
MAX_FILES_TO_PROCESS  = 3       # default number of files to process

# ------------------ SYSTEM PROMPT --------------------------------------------------
SYSTEM_PROMPT = textwrap.dedent("""
You are an expert Agile business-analyst AI.

OBJECTIVE  
Turn the plain-text SMART User Handbook (supplied in the next message) into the most granular set of INVEST-quality* user stories possible, each with a short list of testable features.

INSTRUCTIONS  
1. Read the handbook text carefully.  
2. For **every distinct capability, step, or UI action that delivers standalone value**, create one user story.  
   • Treat separate actions in a numbered procedure (e.g., "filter → run report → export") as *different* stories **unless** they must occur together to satisfy the same business value.  
   • If a requirement applies to multiple roles, write one story per role.  
3. Under each story, list 1-5 atomic **features / acceptance-criteria** that a single developer can finish in ≤3 days.  
4. Keep numbering continuous: start with **US-<START_NUM>** and increment for every story you output.

OUTPUT FORMAT — EXACTLY  
### US-<number>
**User story:** As a <type of user>, I want to <do something>, so that <business value>.
**Features:**
- F-1 <concise, testable feature or task>
- F-2 <concise, testable feature or task>
- … (add F-3, F-4, F-5 as needed; stop at 5)

RULES  
* User-story sentence ≤ 25 words.  
* **Do not invent** requirements. Use only what appears in the handbook section provided.  
* Merge true duplicates; otherwise DO NOT merge unrelated needs—aim for *smallest viable slice* of value.  
* Skip pure marketing or background prose.  
* Features must begin with an *imperative verb* (Add, Validate, Redirect, …) and be directly testable.  
* No extra commentary, headings, or blank lines outside the defined format.  
* Preserve handbook order: output stories in the sequence they appear.

(*INVEST=Independent, Negotiable, Valuable, Estimable, Small, Testable)
""").strip()

# ---------- HELPERS ----------------------------------------------------------------

def parse_model_output(markdown: str, source_file: str):
    """
    Extract rows:
      {'User Story Number', 'User Story Description', 'Feature Number', 'Feature Description', 'Source File'}
    Assumes model followed strict format.
    """
    rows, current_us_num, current_us_desc = [], None, None
    for line in markdown.splitlines():
        line = line.strip()
        # story header
        m = re.match(r"###\s*(US-\d+)", line)
        if m:
            current_us_num = m.group(1)
            current_us_desc = None  # wait for next line
            continue
        # user story description
        if line.lower().startswith("**user story:**"):
            current_us_desc = re.sub(r"^\*\*User story:\*\*\s*", "", line, flags=re.I)
            continue
        # feature lines
        m = re.match(r"-\s*(F-\d+)\s+(.*)", line)
        if m and current_us_num and current_us_desc:
            rows.append({
                "User Story Number": current_us_num,
                "User Story Description": current_us_desc,
                "Feature Number": m.group(1),
                "Feature Description": m.group(2).strip(),
                "Source File": source_file
            })
    return rows

def call_openai(messages):
    """One wrapper, handles simple retry."""
    client = OpenAI()
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 2:
                raise
            print(f"⚠️  OpenAI error ({e}); retrying …")
            time.sleep(2 + attempt)

def process_file(file_path, next_story_num):
    """Process a single file and return the extracted rows."""
    print(f"📖  Reading file: {file_path}")
    text = Path(file_path).read_text(encoding="utf-8")

    print(f"🔎  Processing file to extract user stories (starting with US-{next_story_num})...")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"(Continue numbering beginning with US-{next_story_num})\n\n{text}"}
    ]

    md = call_openai(messages)
    rows = parse_model_output(md, file_path.name)
    return rows

# ---------- MAIN -------------------------------------------------------------------

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("❌  OPENAI_API_KEY not found in .env file or environment variables.")

    # Get number of files to process from command line argument
    num_files = int(sys.argv[1]) if len(sys.argv) > 1 else MAX_FILES_TO_PROCESS
    
    # Setup paths
    output_dir = Path("/Users/ericchasin/github/sentivera/sentivera-agentic-examples/hudsmart/parse-chapters/output")
    final_csv = output_dir / "hud-userstories.csv"
    
    # Get list of txt files
    txt_files = sorted([f for f in output_dir.glob("part_*.txt")])
    if not txt_files:
        sys.exit("❌  No part_*.txt files found in output directory")
    
    # Process files
    all_rows = []
    next_story_num = 1
    
    for i, txt_file in enumerate(txt_files[:num_files], 1):
        print(f"\nProcessing file {i}/{num_files}: {txt_file.name}")
        try:
            rows = process_file(txt_file, next_story_num)
            all_rows.extend(rows)
            
            # Update next story number
            if rows:
                nums = [int(r["User Story Number"].split("-")[1]) for r in rows]
                next_story_num = max(nums) + 1
            
            # Save progress after each file
            df = pd.DataFrame(all_rows)
            df.to_csv(final_csv, index=False, quoting=csv.QUOTE_ALL)
            print(f"✅  Progress saved: {len(df)} total rows written to {final_csv}")
            
            time.sleep(PAUSE_BETWEEN_CALLS)
            
        except Exception as e:
            print(f"❌  Error processing {txt_file.name}: {e}")
            continue

    print(f"\n🎉  Completed processing {num_files} files")
    print(f"📊  Total user stories extracted: {len(all_rows)}")
    print(f"💾  Results saved to: {final_csv}")

if __name__ == "__main__":
    main()
