# omega_ars.py — Omega ARS (Central Relay System)

from chema import inject_chema, query_chembus, decay_chembus
from elema import emit_elema, query_elema, decay_elema, elrec_accept

# === Internal State ===
connected_ars = {}         # References to other ARS modules by sigil
chembus_omega = []         # Omega chembus

SIGIL = "Ω"

# === Pulse Receiver ===
def receive_pulse(spike_packet):
    """
    Accepts incoming spike packets from other ARS systems or global mods.
    Routes spikes to target ARS or handles global sync logic.
    """
    elrec_accept(spike_packet, target="omega")

    # Decay on pulse
    decay_chembus("omega")
    decay_elema("omega")

# === Register External ARS Systems ===
def link_ars(sigil, ars_ref):
    connected_ars[sigil] = ars_ref

# === Push Elema to Other ARS ===
def push_elema_to_all(spike_packet):
    for sigil, ars in connected_ars.items():
        ars.receive_pulse(spike_packet)

# === Pull Chema from All ARS ===
def pull_chema_from_all():
    for sigil, ars in connected_ars.items():
        remote_chema = ars.get_chema()
        inject_chema(remote_chema, target="omega")

# === Allow ARS Modules to Pull Omega Chema ===
def get_chema():
    return query_chembus("omega")

# === Receive Chema from Other ARS (if pushed manually) ===
def receive_chema(chema_packet, from_sigil=None):
    inject_chema(chema_packet, target="omega")

# === Utility: Get Connected ARS ===
def get_connected():
    return list(connected_ars.keys())
