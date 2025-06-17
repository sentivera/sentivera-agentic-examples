import os
from pathlib import Path

def create_output_directory():
    """Create the output directory if it doesn't exist."""
    script_dir = Path(__file__).parent.absolute()
    output_dir = script_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def split_content(input_file, output_dir, chunk_size=20000):
    """Split the input file into smaller files of specified character size."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into chunks
    chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]
    
    # Write each chunk to a separate file
    for i, chunk in enumerate(chunks, 1):
        output_file = output_dir / f"part_{i:03d}.txt"
        with open(output_file, 'w', encoding='utf-8') as out_f:
            out_f.write(chunk)
        print(f"Created file: {output_file}")

def main():
    # Get the absolute path of the current script
    script_dir = Path(__file__).parent.absolute()
    input_file = script_dir.parent / "text_output" / "SMART User Manual.1635279680819.txt"
    output_dir = create_output_directory()
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    print(f"Splitting file {input_file} into chunks of 20000 characters")
    split_content(input_file, output_dir)
    print(f"Files have been created in {output_dir}")

if __name__ == "__main__":
    main()
