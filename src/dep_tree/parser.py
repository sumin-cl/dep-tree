import ast
from pathlib import Path

def parse_file(path: Path):
    """Return the AST for a Python file."""
    text = path.read_text(encoding="utf-8")
    return ast.parse(text)

def get_imports(path: Path):
    tree = parse_file(path)
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports
