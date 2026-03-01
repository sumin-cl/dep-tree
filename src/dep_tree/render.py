from pathlib import Path

def print_dependency_tree(graph: dict[Path, list[Path]]):
    imported = {dep for deps in graph.values() for dep in deps}
    roots = [f for f in graph.keys() if f not in imported]

    visited = set()

    def print_subtree(node: Path, prefix=""):
        print(prefix + node.name)
        visited.add(node)

        children = graph.get(node, [])
        for i, child in enumerate(children):
            connector = "└── " if i == len(children) - 1 else "├── "
            new_prefix = prefix + ("    " if i == len(children) - 1 else "│   ")
            print(prefix + connector + child.name)
            if child not in visited:
                print_subtree(child, new_prefix)

    for root in sorted(roots, key=lambda p: p.name):
        print_subtree(root)


import sys

def progress_bar(current, total, width=40):
    ratio = current / total
    filled = int(ratio * width)
    bar = "█" * filled + "-" * (width - filled)
    percent = int(ratio * 100)
    sys.stdout.write(f"\r[{bar}] {percent}% ({current}/{total})")
    sys.stdout.flush()
    if current == total:
        print()
