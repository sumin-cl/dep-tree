from pathlib import Path
from dep_tree.parser import get_imports
from dep_tree.scanner import find_python_files
from dep_tree.render import progress_bar
from dep_tree.utils import progress

def module_name_from_path(root: Path, file: Path) -> str:
    """Convert a file path into a dotted module name."""
    rel = file.relative_to(root)
    parts = rel.with_suffix("").parts
    return ".".join(parts)

def build_module_index(root: Path):
    """Map module names to file paths."""
    files = find_python_files(root)
    index = {}

    for f in files:
        mod = module_name_from_path(root, f)
        index[mod] = f

    return index

def build_dependency_graph(root: Path):
    root = Path(root)

    files = find_python_files(root)
    total = len(files)
    progress("Scanning", total, total) 

    imports_map = {}
    for i, f in enumerate(files, start=1):
        imports_map[f] = get_imports(f)
        progress("Parsing imports", i, total)

    module_index = build_module_index(root)
    graph = {}
    for i, f in enumerate(files, start=1):
        resolved = [module_index[imp] for imp in imports_map[f] if imp in module_index]
        graph[f] = resolved
        progress("Resolving graph", i, total)

    return graph
