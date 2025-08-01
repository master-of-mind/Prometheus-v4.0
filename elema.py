# elema.py — Synthetic Spike Engine

import time
from collections import defaultdict

# === Elema Storage ===
elema_matrix = {
    "local": [],
    "omega": []
}

# === Emit Elema Spike ===
def emit_elema(spike_dict, target="local"):
    """
    Adds a spike event to the elema matrix.
    Each spike must include: sigil, amp, origin
    Optional: phase, timestamp, sync_id
    """
    if target not in elema_matrix:
        elema_matrix[target] = []

    spike = {
        "sigil": spike_dict.get("sigil"),
        "amp": spike_dict.get("amp", 1),
        "origin": spike_dict.get("origin"),
        "phase": spike_dict.get("phase", 0),
        "timestamp": spike_dict.get("timestamp", time.time()),
        "sync_id": spike_dict.get("sync_id", None),
        "mod_id": spike_dict.get("mod_id", None),
        "triggered_by": spike_dict.get("triggered_by", None),
        "priority": spike_dict.get("priority", 0),
        "target": spike_dict.get("target", None)
    }

    elema_matrix[target].append(spike)

# === Elema Decay ===
def decay_elema(target="local", max_len=10):
    """
    Trims elema list to most recent N spikes.
    """
    if target in elema_matrix:
        while len(elema_matrix[target]) > max_len:
            elema_matrix[target].pop(0)

# === Elema Query ===
def query_elema(target="local"):
    """
    Returns current elema list for given target.
    """
    return elema_matrix.get(target, [])

# === Elema Match Test ===
def elrec_test(sync_conditions, target="local"):
    """
    Checks if recent elema match provided conditions.
    Conditions can include: sigil, mod_id, phase, sync_id
    """
    for spike in reversed(elema_matrix.get(target, [])):
        match = all(spike.get(k) == v for k, v in sync_conditions.items())
        if match:
            return True
    return False

# === Elema Compression Snapshot ===
def compress_elema(target="local"):
    """
    Returns summary stats from elema: spike counts per sigil.
    """
    counts = defaultdict(int)
    for spike in elema_matrix.get(target, []):
        sigil = spike.get("sigil")
        if sigil:
            counts[sigil] += 1
    return dict(counts)
