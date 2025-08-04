import json
import os
import random

class LaptopBody:
    def __init__(self, config_file="laptop_body.json"):
        self.config_file = config_file
        self.state = {}
        self.load_state()

    def load_state(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file not found: {self.config_file}")
        with open(self.config_file, "r") as f:
            self.state = json.load(f)

    def save_state(self):
        with open(self.config_file, "w") as f:
            json.dump(self.state, f, indent=4)

    # ---------- Simulation Update Methods ----------
    def tick(self):
        """Randomly change vitals slightly to simulate fluctuations."""
        self.state["cpu_temp"] = self._fluctuate(self.state["cpu_temp"], 0.5)
        self.state["cpu_load"] = self._fluctuate(self.state["cpu_load"], 2)
        self.state["battery"] = self._fluctuate(self.state["battery"], -0.05)  # drain slowly
        self.save_state()

    def _fluctuate(self, value, change):
        return max(0, min(100, value + random.uniform(-change, change)))

    # ---------- Read Methods (for sensor mods) ----------
    def get_cpu_temp(self):
        return self.state["cpu_temp"]

    def get_cpu_load(self):
        return self.state["cpu_load"]

    def get_battery(self):
        return self.state["battery"]

    def get_fan_rpm(self):
        return self.state["fan_rpm"]

    def get_memory_usage(self):
        return self.state["memory_usage"]

    def get_screen_brightness(self):
        return self.state["screen_brightness"]
