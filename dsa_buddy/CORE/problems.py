import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "problems")

def list_slugs():
    return [f.replace(".json", "") for f in os.listdir(DATA_DIR) if f.endswith(".json")]

def get(slug):
    path = os.path.join(DATA_DIR, slug + ".json")
    with open(path) as f:
        return json.load(f)
