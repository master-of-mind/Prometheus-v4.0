# omega_ars.py — Omega ARS (Central Relay System)

from chema import ChemaBus
from elema import ElemaPacket

class OmegaARS:
    def __init__(self):
        self.chema_bus = ChemaBus()
        self.elema_matrix = []  # Stores history of incoming elema packets for Hz and strength analysis
        self.ars_refs = {}  # Dictionary of other ARS modules keyed by sigil

    def register_ars(self, sigil, ars_module):
        """Register an ARS module (delta, theta, etc.) for cross-communication."""
        self.ars_refs[sigil] = ars_module

    def receive_elema(self, elema: ElemaPacket):
        """Receives elema from other ARS modules or mods, stores and forwards."""
        self.elema_matrix.append(elema.data)
        self._push_elema(elema)

    def _push_elema(self, elema: ElemaPacket):
        """Push the elema to each ARS module specified in the matrix."""
        for i, val in enumerate(elema.data):
            if val > 0:
                sigil = self._index_to_sigil(i)
                if sigil in self.ars_refs:
                    self.ars_refs[sigil].receive_elema(elema)

    def pull_chema(self):
        """Allow external modules to pull the current omega chema."""
        return self.chema_bus.read()

    def receive_chema(self, chema_packet):
        """Store incoming chema packet into Omega's chema bus."""
        self.chema_bus.insert(chema_packet)

    def decay(self):
        """Run chema decay logic."""
        self.chema_bus.decay()

    def _index_to_sigil(self, index):
        sigils = ['δ', 'θ', 'α', 'β', 'γ', 'Ω']
        return sigils[index] if 0 <= index < len(sigils) else None
