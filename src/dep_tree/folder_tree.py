from pathlib import Path
from datetime import datetime
from dep_tree.utils import IGNORED_DIRS, IGNORED_SUFFIXES

def format_file_info(path: Path):
    size_kb = path.stat().st_size / 1024
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    timestamp = mtime.strftime("%Y-%m-%d %H:%M")
    return f" ({size_kb:.1f} KB, {timestamp})"

def build_folder_tree(root: Path, prefix=""):
    lines = []

    entries = list(root.iterdir())
    dirs = sorted([e for e in entries if e.is_dir() and e.name not in IGNORED_DIRS], key=lambda p: p.name.lower())
    files = sorted([e for e in entries if e.is_file()], key=lambda p: p.name.lower())

    ordered = dirs + files

    for i, entry in enumerate(ordered):
        if any(suffix in entry.name for suffix in IGNORED_SUFFIXES):
            continue

        connector = "└── " if i == len(ordered) - 1 else "├── "
        line = prefix + connector + entry.name

        if entry.is_file():
            line += format_file_info(entry)

        lines.append(line)

        if entry.is_dir():
            new_prefix = prefix + ("    " if i == len(ordered) - 1 else "│   ")
            lines.extend(build_folder_tree(entry, new_prefix))

    return lines

def print_folder_tree(root: Path):
    for line in build_folder_tree(root):
        print(line)

from dep_tree.utils import get_output_dir, timestamp

def save_folder_tree(root, base_filename="folder_tree"):
    out_dir = get_output_dir()
    filename = f"{timestamp()}_{base_filename}.txt"
    output_path = out_dir / filename

    lines = build_folder_tree(root)
    output_path.write_text("\n".join(lines), encoding="utf-8")

    return output_path
