"""Content loader — merges every category module file into one catalog."""
import importlib, os
from content.categories import CATEGORIES

_HERE = os.path.dirname(os.path.abspath(__file__))

def load_modules():
    mods = []
    d = os.path.join(_HERE, "modules")
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".py") and not fn.startswith("_"):
            m = importlib.import_module("content.modules." + fn[:-3])
            mods.extend(getattr(m, "MODULES", []))
    return mods

MODULES = load_modules()
BY_ID = {m["id"]: m for m in MODULES}

def by_cat(cat):
    return [m for m in MODULES if m["cat"] == cat]

def stats():
    return {
        "categories": len(CATEGORIES),
        "modules": len(MODULES),
        "theory": sum(len(m.get("theory", [])) for m in MODULES),
        "quiz": sum(len(m.get("quiz", [])) for m in MODULES),
        "labs": sum(len(m.get("labs", [])) for m in MODULES),
        "points": sum(m.get("points", 0) for m in MODULES),
    }
