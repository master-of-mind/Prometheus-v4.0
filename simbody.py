import json
import os
import random
import psutil
from elema import ElemaPulse

class SimBody:
    def __init__(self, config_file="simbody.json", simulation=True):
        self.config_file = config_file
        self.simulation = simulation
        self.state = {}
        self.last_state = {}
        self.sensors = {}  # mapping: vital_name -> list of sensor instances
        self.load_state()

    def load_state(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file not found: {self.config_file}")
        with open(self.config_file, "r") as f:
            self.state = json.load(f)
        self.last_state = self.state.copy()

    def save_state(self):
        with open(self.config_file, "w") as f:
            json.dump(self.state, f, indent=4)

    def register_sensor(self, vital_name, sensor_instance):
        """Register a sensor to listen for changes in a specific vital."""
        if vital_name not in self.sensors:
            self.sensors[vital_name] = []
        self.sensors[vital_name].append(sensor_instance)

    def tick(self):
        """Update vitals and notify sensors."""
        if self.simulation:
            # Simulate fluctuations
            for vital, change in {
                "cpu_temp": 0.5,
                "cpu_load": 2,
                "battery": -0.05,
                "fan_rpm": 50,
                "memory_usage": 1
            }.items():
                self.state[vital] = self._fluctuate(self.state[vital], change)
        else:
            # Real hardware readings
            self.state["cpu_temp"] = self._get_real_cpu_temp()
            self.state["cpu_load"] = psutil.cpu_percent()
            batt = psutil.sensors_battery()
            self.state["battery"] = batt.percent if batt else None
            self.state["fan_rpm"] = self._get_real_fan_rpm()
            self.state["memory_usage"] = psutil.virtual_memory().percent

        self.save_state()
        self._notify_sensors()

    def _fluctuate(self, value, change):
        return max(0, min(100, value + random.uniform(-change, change)))

    def _get_real_cpu_temp(self):
        temps = psutil.sensors_temperatures()
        return temps.get('coretemp', [])[0].current if 'coretemp' in temps else None

    def _get_real_fan_rpm(self):
        fans = psutil.sensors_fans()
        if fans:
            first_sensor = list(fans.keys())[0]
            return fans[first_sensor][0].current
        return None

    def _notify_sensors(self):
        for vital, new_value in self.state.items():
            old_value = self.last_state.get(vital)
            if old_value is None or abs(new_value - old_value) > 1:
                if vital in self.sensors:
                    for sensor in self.sensors[vital]:
                        pulse = ElemaPulse(origin="SimBody", destination=[1,0,0,0,0,0], matrix=[1,0,0,0,0,0])
                        sensor.receive_pulse(pulse)
            self.last_state[vital] = new_value

    # Getter methods
    def get_cpu_temp(self): return self.state["cpu_temp"]
    def get_cpu_load(self): return self.state["cpu_load"]
    def get_battery(self): return self.state["battery"]
    def get_fan_rpm(self): return self.state["fan_rpm"]
    def get_memory_usage(self): return self.state["memory_usage"]
    def get_screen_brightness(self): return self.state["screen_brightness"]
