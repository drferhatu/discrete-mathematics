"""
Make a lab's starter file from its solution: every top-level function body after the docstring
becomes "# TODO / raise NotImplementedError". Everything else (imports, comments, the __main__ demo)
is copied unchanged.

    python scripts/make_starter.py private/solutions/lab07/sets_lab.py labs/templates/lab07/sets_lab.py
"""
import ast
import sys
from pathlib import Path


def make_starter(src: str) -> str:
    lines = src.splitlines(keepends=True)
    tree = ast.parse(src)
    # replace from the bottom up so earlier line numbers stay valid
    for fn in sorted((n for n in tree.body if isinstance(n, ast.FunctionDef)), key=lambda n: -n.lineno):
        body = fn.body
        has_doc = isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) and isinstance(body[0].value.value, str)
        start = body[1].lineno - 1 if has_doc and len(body) > 1 else body[0].lineno - 1
        end = fn.end_lineno
        indent = " " * (fn.col_offset + 4)
        lines[start:end] = [f"{indent}# TODO\n", f"{indent}raise NotImplementedError\n"]
    return "".join(lines)


if __name__ == "__main__":
    solution, starter = map(Path, sys.argv[1:3])
    starter.write_text(make_starter(solution.read_text()))
    print(f"wrote {starter}")
