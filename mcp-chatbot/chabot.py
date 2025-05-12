# chatbot.py
from tools.math_tool import math_tool
from steps.mcp_step import create_mcp_step

TOOL_REGISTRY = {
    "math_tool": math_tool
}

def handle_step(step):
    tool_name = step.get("tool_name")
    tool = TOOL_REGISTRY.get(tool_name)
    if not tool:
        return "Unknown tool"
    return tool(step["input"])

def run_chatbot():
    print("Welcome to MCP Chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        step = create_mcp_step(user_input)
        response = handle_step(step)
        print(f"Bot: {response}")

if __name__ == "__main__":
    run_chatbot()
