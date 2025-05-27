An AST (Abstract Syntax Tree) Parser typically outputs a hierarchical tree structure that represents the syntactic structure of source code. Here's what an AST Parser commonly outputs:
Core Structure

Tree representation of code with nodes representing language constructs
Parent-child relationships showing code hierarchy
Node types (expressions, statements, declarations, etc.)
Source location information (line numbers, column positions, file paths)

Typical AST Node Information

Identifiers: Variable names, function names, class names
Declarations: Functions, classes, variables, imports
Expressions: Binary operations, function calls, literals
Statements: If/else, loops, try/catch, return statements
Type information (in typed languages)
Scope boundaries and variable bindings

Common Output Formats

JSON/XML tree structure with nested nodes
Graph representation with node IDs and relationships
Visitor pattern objects for traversal
Symbol tables mapping identifiers to their definitions

Example AST Output (simplified):
json{
  "type": "Program",
  "body": [
    {
      "type": "FunctionDeclaration",
      "name": "calculateTotal",
      "params": ["price", "tax"],
      "body": {
        "type": "BlockStatement",
        "statements": [...]
      },
      "location": {"line": 15, "column": 1}
    }
  ]
}
