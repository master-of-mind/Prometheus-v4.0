class Chrec:
    def __init__(self):
        self.locked_conditions = []  # List of condition sets (chema to match)
    
    def add_condition(self, chemlock):
        """Add a new chemlock condition."""
        self.locked_conditions.append(chemlock)

    def test_lock(self, chema_packet):
        """
        Test if the chema packet satisfies any of the locked conditions.
        Returns a boolean indicating whether any lock was triggered.
        """
        for chemlock in self.locked_conditions:
            if self.match_chema(chema_packet, chemlock):
                return True
        return False

    def match_chema(self, chema_packet, chemlock):
        """
        Checks if the provided chema packet matches the condition of the chemlock.
        The chemlock and chema packet should be in the same format, i.e., they should be dictionaries.
        """
        # Iterate through the chemlock and check if the values match
        for key, value in chemlock.items():
            if key not in chema_packet:
                return False  # The chema packet doesn't contain the necessary key
            if chema_packet[key] != value:
                return False  # The value does not match
        return True

    def clear_locks(self):
        """Clears all the stored conditions."""
        self.locked_conditions.clear()
