from pathlib import Path
from dep_tree.utils import IGNORED_DIRS, IGNORED_SUFFIXES

def find_python_files(root: Path):
    files = []
    for path in root.rglob("*.py"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if any(suffix in path.parts for suffix in IGNORED_SUFFIXES):
            continue
        files.append(path)
    return files
