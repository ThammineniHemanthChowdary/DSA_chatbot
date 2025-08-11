import ast
import json
import subprocess
import sys
import tempfile
import textwrap
import os
from typing import List, Dict, Any

# ---- Simple safety gates (beginner-friendly) ----
FORBIDDEN_NODES = (ast.Import, ast.ImportFrom, ast.With, ast.Try, ast.Raise, ast.Global, ast.Nonlocal)

def _validate_user_code(src: str):
    tree = ast.parse(src, mode="exec")
    for node in ast.walk(tree):
        if isinstance(node, FORBIDDEN_NODES):
            raise ValueError("Disallowed syntax (imports/with/try/etc. are blocked in this runner).")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "__import__"}:
            raise ValueError("Disallowed call (eval/exec/__import__).")
    return True

PY_TEMPLATE = """
{user_code}

# glue
TARGET = {func_name}

import json, sys, time, tracemalloc
def __run_one(test):
    args = test["input"]
    return TARGET(**args)

def __main():
    cases = json.loads(sys.stdin.read())
    tracemalloc.start()
    start_ns = time.perf_counter_ns()
    results = []
    for t in cases:
        results.append(__run_one(t))
    elapsed_ms = max(1, int((time.perf_counter_ns() - start_ns) / 1_000_000))
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(json.dumps({{"ok": True, "results": results, "elapsed_ms": elapsed_ms, "peak_mem_kb": int(peak/1024)}}))

if __name__ == "__main__":
    __main()
"""



def run_python(user_code: str, func_name: str, tests: List[Dict[str, Any]], timeout_s: int = 2) -> Dict[str, Any]:
    _validate_user_code(user_code)
    program = PY_TEMPLATE.format(user_code=user_code, func_name=func_name)
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(program)
        path = f.name
    try:
        p = subprocess.Popen(
            [sys.executable, path],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True
        )
        out, err = p.communicate(input=json.dumps(tests), timeout=timeout_s)
        if p.returncode != 0:
            return {"ok": False, "error": (err or out)[:2000]}
        return json.loads(out)
    except subprocess.TimeoutExpired:
        p.kill()
        return {"ok": False, "error": "Time Limit Exceeded"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        try: os.remove(path)
        except: pass
