# elema.py — Synthetic Spike Engine

# elema.py

from collections import defaultdict
import json

SIGIL_ORDER = ['δ', 'θ', 'α', 'β', 'γ', 'Ω']

class Elema:
    def __init__(self):
        self.spikes = []

    def emit_spike(self, sigil_matrix, origin, amp=1.0, phase=0, sync_id=None):
        """
        Emits a spike into the system.
        sigil_matrix: list of 6 values (-1, 0, 1) showing directionality
        origin: string name of the mod or system
        amp: intensity (float)
        phase: optional phase data (int)
        sync_id: optional tag for chaining/sync
        """
        key = self._compress_matrix(sigil_matrix)
        spike = {
            "matrix": key,
            "origin": origin,
            "amp": amp,
            "phase": phase,
            "sync_id": sync_id
        }
        self.spikes.append(spike)

    def pull_spikes(self, target_sigil):
        """
        Pull all spikes that include this sigil in their matrix.
        """
        idx = SIGIL_ORDER.index(target_sigil)
        relevant = []
        for spike in self.spikes:
            if self._decompress_matrix(spike['matrix'])[idx] != 0:
                relevant.append(spike)
        return relevant

    def decay_spikes(self, decay_rate=0.1):
        """
        Gradually erases older spikes (based on amp), unless they’re reinforced.
        """
        decayed = []
        for spike in self.spikes:
            spike['amp'] -= decay_rate
            if spike['amp'] > 0.01:
                decayed.append(spike)
        self.spikes = decayed

    def _compress_matrix(self, matrix):
        """
        Same format as chema—compressed string like θ:1,β:-1
        """
        return ','.join(f"{SIGIL_ORDER[i]}:{v}" for i, v in enumerate(matrix) if v != 0)

    def _decompress_matrix(self, matrix_str):
        """
        Converts compressed string back to list.
        """
        m = [0] * 6
        if not matrix_str:
            return m
        parts = matrix_str.split(',')
        for part in parts:
            sigil, val = part.split(':')
            m[SIGIL_ORDER.index(sigil)] = int(val)
        return m

    def dump(self):
        return json.dumps(self.spikes, indent=2)
