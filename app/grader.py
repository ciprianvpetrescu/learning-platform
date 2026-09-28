"""Answer normalisation and grading for games."""
import re, random

def norm(s):
    s = (s or "").strip().lower()
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c",'"').replace("\u201d",'"')
    s = re.sub(r"\s+", " ", s)
    # strip a trailing period unless it is meaningful (jwt none, etc)
    if s.endswith('.') and not s.endswith('..'):
        s = s[:-1]
    return s

def norm_sql(s):
    """Loose SQL normalisation: collapse whitespace, unify comment syntax."""
    s = norm(s)
    s = s.replace('-- -', '--').replace('--  ', '--').replace('#', '--')
    s = re.sub(r'\s*--+\s*$', '--', s)
    s = s.replace('null', 'null')
    return s

def check_input(game, ch, given):
    g = norm(given)
    if not g:
        return False
    answers = ch.get('answers', [])
    if ch.get('hint') and 'sql' in (game.get('id') or ''):
        g2 = norm_sql(given)
        for a in answers:
            if norm_sql(a) == g2:
                return True
    for a in answers:
        na = norm(a)
        if g == na:
            return True
        # allow numeric equivalence
        try:
            if float(g) == float(na):
                return True
        except Exception:
            pass
    return False

def check_quiz(ch, idx):
    try:
        return int(idx) == int(ch['c'])
    except Exception:
        return False

def check_builder(ch, payload):
    """payload: list of indices (order games) or an int (pick-one games)."""
    if 'order' in ch:
        if not isinstance(payload, list):
            return False
        try:
            p = [int(x) for x in payload]
        except Exception:
            return False
        return p == list(ch['order'])
    if 'correct' in ch:
        try:
            return int(payload) == int(ch['correct'])
        except Exception:
            return False
    return False
