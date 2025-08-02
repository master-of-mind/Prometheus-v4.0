# chema.py — Synthetic Neurochemical Engine

from collections import defaultdict
import json

SIGIL_ORDER = ['δ', 'θ', 'α', 'β', 'γ', 'Ω']

class Chema:
    def __init__(self):
        self.packets = []

    def emit(self, sigil_matrix, compound):
        """
        Emit a new chema packet.
        sigil_matrix: list of 6 ints (-1, 0, 1) representing directionality per ARS sigil
        compound: string label for the chema type, e.g., 'fatigue', 'novelty'
        """
        key = self._compress_matrix(sigil_matrix)
        self.packets.append({
            'compound': compound,
            'matrix': key,
            'count': 1
        })

    def absorb(self, new_packets):
        """
        Merge new packets into the system, combining same-matrix+compound entries.
        """
        merged = defaultdict(lambda: {'compound': None, 'matrix': None, 'count': 0})
        for packet in self.packets + new_packets:
            c = packet['compound']
            m = packet['matrix']
            k = f"{c}:{m}"
            merged[k]['compound'] = c
            merged[k]['matrix'] = m
            merged[k]['count'] += packet.get('count', 1)
        self.packets = list(merged.values())

    def pull(self, target_sigil):
        """
        Returns all chema targeting this ARS sigil.
        """
        idx = SIGIL_ORDER.index(target_sigil)
        return [pkt for pkt in self.packets if self._decompress_matrix(pkt['matrix'])[idx] != 0]

    def decay(self, rate=0.1):
        """
        Decays chema counts, removing near-zero entries.
        """
        decayed = []
        for pkt in self.packets:
            pkt['count'] -= rate
            if pkt['count'] > 0:
                decayed.append(pkt)
        self.packets = decayed

    def neutralize(self):
        """
        Combines chema of the same type with opposing matrices.
        If they sum to zero, removes them.
        """
        pairs = defaultdict(list)
        for pkt in self.packets:
            key = pkt['compound']
            pairs[key].append(pkt)

        new_packets = []
        for key, group in pairs.items():
            merged = defaultdict(int)
            for pkt in group:
                m_key = pkt['matrix']
                merged[m_key] += pkt['count']
            for m_key, count in merged.items():
                if abs(count) > 0.01:
                    new_packets.append({
                        'compound': key,
                        'matrix': m_key,
                        'count': round(count, 2)
                    })
        self.packets = new_packets

    def _compress_matrix(self, matrix):
        """
        Convert a sigil matrix to a compressed string.
        E.g., [1,0,0,0,0,0] => "δ:1"
              [1,0,1,0,0,0] => "δ:1,α:1"
        """
        return ','.join(f"{SIGIL_ORDER[i]}:{v}" for i, v in enumerate(matrix) if v != 0)

    def _decompress_matrix(self, s):
        """
        Converts string back to full matrix.
        """
        m = [0] * 6
        if not s:
            return m
        parts = s.split(',')
        for part in parts:
            sigil, val = part.split(':')
            m[SIGIL_ORDER.index(sigil)] = int(val)
        return m

    def dump(self):
        """
        For inspection or debugging.
        """
        return json.dumps(self.packets, indent=2)
