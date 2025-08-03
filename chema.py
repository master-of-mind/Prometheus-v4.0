# chema.py

from typing import List, Dict, Any
from collections import defaultdict

SIGIL_MAP = {
    1: "δ",  # Delta
    2: "θ",  # Theta
    3: "α",  # Alpha
    4: "β",  # Beta
    5: "γ",  # Gamma
    6: "Ω",  # Omega
}

# -----------------------------
# chema_structure
# -----------------------------
class ChemaPacket:
    def __init__(self, origin: int, dest: int, matrix: List[int]):
        self.origin = origin  # int (sigil number)
        self.dest = dest      # int (sigil number)
        self.matrix = matrix  # List[int] of length 6, values in [-1, 0, 1]
        self.count = 1

    def __repr__(self):
        sigils = "".join(SIGIL_MAP.get(i + 1, "?") for i, val in enumerate(self.matrix) if val != 0)
        return f"<Chema {SIGIL_MAP[self.origin]}→{SIGIL_MAP[self.dest]} {sigils} x{self.count}>"

    def key(self):
        return (self.origin, self.dest, tuple(self.matrix))

# -----------------------------
# compression
# -----------------------------
def compress_chema(packets: List[ChemaPacket]) -> List[ChemaPacket]:
    compressed = {}
    for pkt in packets:
        k = pkt.key()
        if k in compressed:
            compressed[k].count += pkt.count
        else:
            compressed[k] = ChemaPacket(pkt.origin, pkt.dest, pkt.matrix[:])
            compressed[k].count = pkt.count
    return list(compressed.values())

def neutralize_chema(packets: List[ChemaPacket]) -> List[ChemaPacket]:
    tracker = defaultdict(int)
    for pkt in packets:
        k = pkt.key()
        tracker[k] += pkt.count

    result = []
    for (origin, dest, matrix), count in tracker.items():
        if count != 0:
            new_pkt = ChemaPacket(origin, dest, list(matrix))
            new_pkt.count = count
            result.append(new_pkt)
    return result

# -----------------------------
# chema_tools
# -----------------------------
def sum_chema_fields(packets: List[ChemaPacket]) -> Dict[str, int]:
    result = defaultdict(int)
    for pkt in packets:
        for i, val in enumerate(pkt.matrix):
            result[SIGIL_MAP[i + 1]] += val * pkt.count
    return dict(result)

def chrec_match(packets: List[ChemaPacket], chemlock: List[int]) -> int:
    """
    Returns number of chema packets that match the chemlock exactly.
    """
    match_count = 0
    for pkt in packets:
        if pkt.matrix == chemlock:
            match_count += pkt.count
    return match_count

def extract_for_matching(packets: List[ChemaPacket], target_dest: int) -> List[ChemaPacket]:
    return [pkt for pkt in packets if pkt.dest == target_dest]

# -----------------------------
# Public API
# -----------------------------
__all__ = [
    "ChemaPacket",
    "compress_chema",
    "neutralize_chema",
    "sum_chema_fields",
    "chrec_match",
    "extract_for_matching",
    ]
