#elema.py

from collections import deque

class Elema:
    def __init__(self):
        # Each entry is a tuple: (origin_sigil, destination_sigil, amplitude_matrix)
        self.elema_queue = deque()

    def add_elema(self, origin, destination, matrix):
        """Add an elema pulse to the queue"""
        self.elema_queue.append((origin, destination, matrix))

    def get_next_elema(self):
        """Retrieve the next elema pulse from the queue"""
        if self.elema_queue:
            return self.elema_queue.popleft()
        return None

    def peek_all_elema(self):
        """Returns a list of all current elema pulses without removing them"""
        return list(self.elema_queue)

    def clear(self):
        """Empty the queue"""
        self.elema_queue.clear()

    def __len__(self):
        return len(self.elema_queue)

    def __repr__(self):
        return f"<ElemaQueue size={len(self.elema_queue)}>"
