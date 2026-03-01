import sys

IGNORED_DIRS = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "env",
    "site-packages",
    "dist",
    "build",
}

IGNORED_SUFFIXES = {
    ".egg-info",
}

def progress(stage, current, total, width=40):
    ratio = current / total
    filled = int(ratio * width)
    bar = "█" * filled + "-" * (width - filled)
    percent = int(ratio * 100)
    sys.stdout.write(f"\r{stage}: [{bar}] {percent}% ({current}/{total})")
    sys.stdout.flush()
    if current == total:
        print()

from pathlib import Path

def get_output_dir():
    base = Path(__file__).resolve().parent      # src/dep_tree/
    project_root = base.parent.parent           # dep-tree/
    out = project_root / "output"
    out.mkdir(exist_ok=True)
    return out


from datetime import datetime

def timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

