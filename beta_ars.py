# beta_ars.py — Beta ARS (Autonomic Relay System)

from chema import ChemaPacket, decay_and_cleanup_chema
from elema import ElemaPacket, elrec_test
from sigils import SIGIL_BETA

class BetaARS:
    def __init__(self):
        self.chema_bus = []
        self.linked_mods = []
        self.external_ars = {}

    def connect_mod(self, mod):
        self.linked_mods.append(mod)

    def connect_ars(self, sigil, ars):
        self.external_ars[sigil] = ars

    def receive_elema(self, elema: ElemaPacket):
        self.pulse(elema)

    def pulse(self, elema: ElemaPacket):
        decay_and_cleanup_chema(self.chema_bus)
        for mod in self.linked_mods:
            if elrec_test(mod, elema):
                mod.on_pulse(elema)
        self.route_chema()

    def add_chema(self, packet: ChemaPacket):
        self.chema_bus.append(packet)

    def get_chema(self):
        return self.chema_bus

    def route_chema(self):
        to_push = [c for c in self.chema_bus if SIGIL_BETA not in c.destinations]
        for packet in to_push:
            for sigil, ars in self.external_ars.items():
                if sigil in packet.destinations:
                    ars.add_chema(packet)
