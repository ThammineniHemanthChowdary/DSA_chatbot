# core/complexity.py
import ast, math
from typing import Dict, Any, List, Tuple
from .runner import run_python

# --------- 1) Static AST heuristic (quick & friendly) ----------
def estimate_big_o_from_ast(src: str) -> Dict[str, Any]:
    """
    Very rough heuristic:
    - nested loops over the same iterable => O(n^2)
    - sort() / sorted() => likely O(n log n)
    - heapq usage => O(n log n)
    - dict/set membership or indexing seen => tends toward O(n) overall
    """
    tree = ast.parse(src, mode="exec")
    loops = []
    calls = set()
    names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            loops.append(node)
        if isinstance(node, ast.Call):
            # collect function names
            if isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr)
            elif isinstance(node.func, ast.Name):
                calls.add(node.func.id)
        if isinstance(node, ast.Name):
            names.add(node.id)

    evidence = []
    guess = "O(n)"  # default optimistic

    # nested loops -> O(n^2)
    nested = any(any(outer is not inner and hasattr(outer, "body") and inner in ast.walk(outer) 
                     for inner in loops) for outer in loops)
    if nested:
        guess = "O(n^2)"
        evidence.append("nested loops detected")

    # sort or sorted -> O(n log n)
    if "sort" in calls or "sorted" in calls:
        guess = "O(n log n)"
        evidence.append("sort/sorted usage")

    # heapq -> O(n log n)
    for k in ("heappush", "heappop", "heapify"):
        if k in calls:
            guess = "O(n log n)"
            evidence.append("heap operations")

    # hashmap/set usage hints O(1) ops inside a single loop
    if ("dict" in names or "set" in names) and not nested and guess == "O(n)":
        evidence.append("hash table usage")

    return {"static_time": guess, "evidence": evidence}

# --------- 2) Empirical timing by scaling input ----------
def empirical_timing(user_code: str, func_name: str, bench_fn, sizes: List[int]) -> List[Tuple[int, int]]:
    """
    Returns list of (n, avg_elapsed_ms) with a few repeats to smooth noise.
    """
    results = []
    for n in sizes:
        tests = bench_fn(n, repeats=5)   # 5 repeats per size
        res = run_python(user_code, func_name, tests, timeout_s=5)
        if not res.get("ok"):
            results.append((n, -1))
            break
        avg_ms = max(1, int(res.get("elapsed_ms", 0) / max(1, len(tests))))
        results.append((n, avg_ms))
    return results


def slope_loglog(points: List[Tuple[int, int]]) -> float:
    """Compute slope of log(time) vs log(n) ignoring invalid or zero times."""
    valid = [(n, t) for (n, t) in points if n > 0 and t > 0]
    if len(valid) < 2:
        return 0.0
    xs = [math.log(n) for n, _ in valid]
    ys = [math.log(t) for _, t in valid]
    n = len(xs)
    x_mean = sum(xs)/n
    y_mean = sum(ys)/n
    num = sum((xs[i]-x_mean)*(ys[i]-y_mean) for i in range(n))
    den = sum((xs[i]-x_mean)**2 for i in range(n)) or 1e-9
    return num/den

def classify_from_slope(s: float) -> str:
    # Rough buckets; slope ~ 1 => O(n), ~1.3–1.6 => O(n log n), ~2 => O(n^2)
    if s < 1.2:
        return "O(n)"
    if s < 1.8:
        return "O(n log n)"
    return "O(n^2)"

def analyze(user_code: str, func_name: str, problem_slug: str) -> Dict[str, Any]:
    from . import problems as P
    static_est = estimate_big_o_from_ast(user_code)
    bench = P.get_benchmark_generator(problem_slug)
    timing = []
    slope = None
    empirical_class = None
    if bench:
        timing = empirical_timing(user_code, func_name, bench, sizes=[200, 2000, 8000])
        s = slope_loglog(timing)
        slope = round(s, 2)
        empirical_class = classify_from_slope(s)
    return {
        "static_time_guess": static_est["static_time"],
        "static_evidence": static_est["evidence"],
        "empirical_points": timing,           # list of (n, ms)
        "empirical_slope": slope,            # may be None if no bench
        "empirical_time_guess": empirical_class
    }
