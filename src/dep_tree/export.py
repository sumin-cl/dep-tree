import json
from pathlib import Path
from dep_tree.utils import get_output_dir, timestamp

def detect_cycles(graph: dict[Path, list[Path]]):
    visited = set()
    stack = set()
    cycles = []

    def dfs(node, path):
        if node in stack:
            cycle_start = path.index(node)
            cycles.append([str(p) for p in path[cycle_start:]])
            return

        if node in visited:
            return

        visited.add(node)
        stack.add(node)

        for dep in graph.get(node, []):
            dfs(dep, path + [dep])

        stack.remove(node)

    for file in graph:
        dfs(file, [file])

    return cycles

def export_json(graph: dict[Path, list[Path]]):
    out_dir = get_output_dir()
    filename = f"{timestamp()}_deps.json"
    output_path = out_dir / filename

    cycles = detect_cycles(graph)

    data = {
        "files": [
            {
                "file": str(file),
                "imports": [str(dep) for dep in deps]
            }
            for file, deps in graph.items()
        ],
        "cycles": cycles
    }

    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return output_path
