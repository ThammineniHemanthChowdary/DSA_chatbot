import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "problems")

def list_slugs():
    return [f.replace(".json", "") for f in os.listdir(DATA_DIR) if f.endswith(".json")]

def get(slug):
    path = os.path.join(DATA_DIR, slug + ".json")
    with open(path) as f:
        return json.load(f)

# --- Benchmark data generators for empirical timing ---
import random

def _gen_two_sum_case(n: int):
    random.seed(0)
    nums = list(range(n))
    target = (n // 2) + (n // 3)
    nums[n // 2] = n // 3
    nums[n // 3] = n // 2
    return {"input": {"nums": nums, "target": target}, "output": [n // 3, n // 2]}

# Return a callable that, given N, returns a list[dict] of test cases
def get_benchmark_generator(slug: str):
    if slug == "two_sum" or slug == "two-sum":
        def make_tests(n: int, repeats: int = 1):
            return [_gen_two_sum_case(n) for _ in range(repeats)]
        return make_tests
    return None  # fallback if we haven't defined a generator yet

