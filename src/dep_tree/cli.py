from pathlib import Path
from dep_tree.graph import build_dependency_graph
from dep_tree.folder_tree import print_folder_tree, save_folder_tree
from dep_tree.render import print_dependency_tree
from dep_tree.export import export_json

def main():
    import sys

    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("Usage: python -m dep_tree <path> [--folder-out] [--json]")
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()

    if not root.exists(): 
        print(f"Error: Path does not exist: {root}") 
        sys.exit(1)

    print("\n=== Folder Structure ===\n")
    print_folder_tree(root)

    if "--folder-out" in sys.argv:
        saved = save_folder_tree(root)
        print(f"Saved folder structure to {saved}")

    graph = build_dependency_graph(root)

    print("\n=== Dependency Tree ===\n")
    print_dependency_tree(graph)

    if "--json" in sys.argv:
        saved_json = export_json(graph)
        print(f"\nSaved JSON to {saved_json}")
