"""Merges all bank files (python modules and json) into one dict keyed by game id."""
import json, os, importlib

_HERE = os.path.dirname(os.path.abspath(__file__))

BANKS = {}

for fn in sorted(os.listdir(_HERE)):
    if fn.endswith('.json'):
        with open(os.path.join(_HERE, fn)) as f:
            BANKS.update(json.load(f))
    elif fn.endswith('.py') and fn != '__init__.py':
        m = importlib.import_module('games.banks.' + fn[:-3])
        BANKS.update(getattr(m, 'BANKS', {}))
