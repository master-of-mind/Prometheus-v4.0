# elema.py — Synthetic Spike Engine

SIGILS = ["δ", "θ", "α", "β", "γ", "Ω"]

class Elema:
    def __init__(self, values=None):
        # values is a dict with sigils as keys and positive integers as strength
        self.values = {sigil: 0 for sigil in SIGILS}
        if values:
            for k, v in values.items():
                if k in self.values and isinstance(v, int) and v > 0:
                    self.values[k] = v

    def get(self, sigil):
        return self.values.get(sigil, 0)

    def set(self, sigil, strength):
        if sigil in self.values and strength > 0:
            self.values[sigil] = strength

    def to_dict(self):
        return {k: v for k, v in self.values.items() if v > 0}

    def __str__(self):
        return f"<Elema: {self.to_dict()}>"

    def amplify(self, multiplier):
        for k in self.values:
            self.values[k] *= multiplier

    def merge(self, other):
        for k in self.values:
            self.values[k] += other.get(k)

    def is_empty(self):
        return all(v == 0 for v in self.values.values())
