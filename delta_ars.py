# delta_ars.py — Delta ARS (Autonomic Relay System)

from chema import inject_chema, query_chembus, decay_chembus, chrec_trigger
from elema import emit_elema, query_elema, decay_elema, elrec_accept

# === Internal State ===
local_mods = []            # Mods assigned to Delta group
connected_ars = {}         # References to other ARS modules by sigil
chembus_local = []         # Local Delta chembus

SIGIL = "δ"

# === Pulse Receiver ===
def receive_pulse(spike_packet):
    """
    Accepts incoming spike packets from local mods or external ARS.
    Routes spikes and applies chema if needed.
    """
    if spike_packet["sigil"] != SIGIL:
        forward_to_ars(spike_packet)
        return

    elrec_accept(spike_packet, target="local")

    # Notify mods
    for mod in local_mods:
        mod.on_pulse(spike_packet)

    # Apply decay logic (pulse = tick)
    decay_chembus("local")
    decay_elema("local")

# === Forwarding Function ===
def forward_to_ars(spike_packet):
    sigil = spike_packet["sigil"]
    if sigil in connected_ars:
        connected_ars[sigil].receive_pulse(spike_packet)

# === Register Mods ===
def register_mod(mod_ref):
    local_mods.append(mod_ref)

# === Register External ARS Systems ===
def link_ars(sigil, ars_ref):
    connected_ars[sigil] = ars_ref

# === Broadcast Chema to Other ARS ===
def push_chema_to_others(chema_packet):
    for sigil, ars in connected_ars.items():
        ars.receive_chema(chema_packet, from_sigil=SIGIL)

# === Receive Chema from Other ARS ===
def receive_chema(chema_packet, from_sigil=None):
    inject_chema(chema_packet, target="local")

# === Query Local Chembus ===
def get_chema():
    return query_chembus("local")

# === Utility: Get Connected ARS ===
def get_connected():
    return list(connected_ars.keys())
