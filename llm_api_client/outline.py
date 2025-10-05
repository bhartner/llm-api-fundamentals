"""
Outline functions of py file for documentation via command line
"""
import ast
import sys
import os # Import os for file existence check

def get_def_names(file_path):
    """Parses a Python file and returns a list of function and class names."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error parsing file: {e}", file=sys.stderr)
        return []

    names = []
    for node in ast.walk(tree):
        # Extract function names
        if isinstance(node, ast.FunctionDef):
            names.append(f"Function: {node.name}")
        # Extract class names
        elif isinstance(node, ast.ClassDef):
            names.append(f"Class: {node.name}")

    return names

# --- Execution Block ---
if __name__ == "__main__":
    # Check if a file path was provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python outline.py <path_to_python_file.py>", file=sys.stderr)
        sys.exit(1)

    file_to_check = sys.argv[1] # The first argument after the script name
    definitions = get_def_names(file_to_check)

    if definitions:
        print(f"\n--- Definitions in {file_to_check} ---")
        for name in definitions:
            print(name)
        print("----------------------------------------\n")