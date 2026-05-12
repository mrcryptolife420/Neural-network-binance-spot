from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


def _module_name(root: Path, path: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    return ".".join(rel.parts)


def build_code_graph(root: Path | str = ".", out: Path | str | None = None) -> dict[str, Any]:
    root_path = Path(root).resolve()
    src_root = root_path / "src" / "binance_spot_bot"
    files = sorted(src_root.rglob("*.py")) if src_root.exists() else []
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []
    fan_in: dict[str, int] = {}
    fan_out: dict[str, int] = {}
    symbols: list[dict[str, str]] = []
    for path in files:
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        module = path.name
        full_module = _module_name(src_root, path)
        nodes.append({"id": module, "module": full_module, "path": path.relative_to(root_path).as_posix(), "lines": text.count("\n") + 1})
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                symbols.append({"module": module, "name": node.name, "type": node.__class__.__name__})
            if isinstance(node, ast.ImportFrom):
                base = node.module or ""
                if node.level and base:
                    target = base.split(".")[-1] + ".py"
                    edges.append({"source": module, "target": target, "type": "imports_from"})
                    fan_out[module] = fan_out.get(module, 0) + 1
                    fan_in[target] = fan_in.get(target, 0) + 1
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("binance_spot_bot."):
                        target = alias.name.rsplit(".", 1)[-1] + ".py"
                        edges.append({"source": module, "target": target, "type": "imports"})
                        fan_out[module] = fan_out.get(module, 0) + 1
                        fan_in[target] = fan_in.get(target, 0) + 1
    high_fan_in = sorted([{"module": key, "count": value} for key, value in fan_in.items() if value >= 5], key=lambda item: item["count"], reverse=True)
    high_fan_out = sorted([{"module": key, "count": value} for key, value in fan_out.items() if value >= 10], key=lambda item: item["count"], reverse=True)
    payload = {
        "status": "ready",
        "payload": {
            "nodes": [item["id"] for item in nodes],
            "module_nodes": nodes,
            "edges": edges,
            "symbols": symbols,
            "high_fan_in": high_fan_in,
            "high_fan_out": high_fan_out,
            "large_modules": [item for item in nodes if item["lines"] > 700],
            "cycles": [],
        },
        "live_trading_enabled": False,
    }
    if out:
        out_path = Path(out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return payload


def code_graph(root: Path | str = ".") -> dict[str, Any]:
    return build_code_graph(root)
