# gamma_ars.py — Gamma ARS (Autonomic Relay System)

from chema import receive_chema
from elema import elrec_accept

class GammaARS:
    def __init__(self):
        self.sigil = "γ"
        self.mods = []
        self.chema_bus = []
        self.linked_ars = {}

    def add_mod(self, mod):
        self.mods.append(mod)

    def link_ars(self, sigil, ars_ref):
        self.linked_ars[sigil] = ars_ref

    def receive_pulse(self, spike_packet):
        if not elrec_accept(spike_packet, self.sigil):
            return

        new_spikes = []
        new_chema = []

        for mod in self.mods:
            spikes, chema = mod.on_pulse(spike_packet)
            new_spikes.extend(spikes)
            new_chema.extend(chema)

        for spike in new_spikes:
            for sigil, ars in self.linked_ars.items():
                ars.receive_pulse(spike)

        for chem in new_chema:
            destination = chem.get("destination_sigil")
            if destination in self.linked_ars:
                self.linked_ars[destination].receive_chema(chem)

    def receive_chema(self, chem_packet):
        self.chema_bus.append(chem_packet)

    def get_chema(self):
        return self.chema_bus
