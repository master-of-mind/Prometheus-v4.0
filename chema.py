# chema.py — Synthetic Neurochemical Engine

from collections import defaultdict

# === Chembus Storage ===
chembus_map = {
    "local": [],
    "omega": []
}

# === Inject Chema ===
def inject_chema(packet, target="local"):
    """
    Adds a chema packet to the specified chembus.
    Each packet is a dict of {key: value} where value is -1, 0, or 1.
    """
    if target not in chembus_map:
        chembus_map[target] = []
    chembus_map[target].append(packet)

# === Compress Chembus ===
def compress_chema(chembus):
    """
    Sums repeated chema values into a single dict.
    """
    counter = defaultdict(int)
    for packet in chembus:
        for k, v in packet.items():
            counter[k] += v
    return dict(counter)

# === Chrec Trigger ===
def chrec_trigger(chemlock, target="local"):
    """
    Checks if the compressed chema matches the chemlock.
    Returns (True, match_count) if all chemlock keys are matched.
    """
    compressed = compress_chema(chembus_map[target])
    match_count = 0
    for k, v in chemlock.items():
        if k not in compressed:
            return False, 0
        if compressed[k] * v < 1:
            return False, 0
        match_count += 1
    return True, match_count

# === Chembus Decay ===
def decay_chembus(target="local", max_len=10):
    """
    Trims the chembus to a maximum length.
    """
    if target in chembus_map:
        while len(chembus_map[target]) > max_len:
            chembus_map[target].pop(0)

# === Chembus Query ===
def query_chembus(target="local"):
    """
    Returns the current chembus list.
    """
    return chembus_map.get(target, [])

# === Chembus Compression Snapshot ===
def get_compressed_state(target="local"):
    return compress_chema(query_chembus(target))
