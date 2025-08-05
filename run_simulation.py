import time

# ARS modules
from delta_ars import DeltaARS
from theta_ars import ThetaARS
from alpha_ars import AlphaARS
from beta_ars import BetaARS
from gamma_ars import GammaARS
from omega_ars import OmegaARS

# Sensors
from cpu_temp import CPUTemp
from cpu_load import CPULoad
from battery import Battery
from fan_speed import FanSpeed
from ram_usage import RAMUsage

# Simulated body
from simbody import SimBody

# Pulse type
from elema import ElemaPulse


def link_ars_modules(delta, theta, alpha, beta, gamma, omega):
    """Wire ARS modules so they can pass pulses & chema between each other."""
    modules = [delta, theta, alpha, beta, gamma, omega]
    for src in modules:
        for dst in modules:
            if src is not dst:
                src.link_ars(dst)


if __name__ == "__main__":
    print("🚀 Starting Prometheus in full simulation mode...")

    # ---- Initialize ARS modules ----
    delta_ars = DeltaARS()
    theta_ars = ThetaARS()
    alpha_ars = AlphaARS()
    beta_ars = BetaARS()
    gamma_ars = GammaARS()
    omega_ars = OmegaARS()

    # ---- Wire ARS interconnections ----
    link_ars_modules(delta_ars, theta_ars, alpha_ars, beta_ars, gamma_ars, omega_ars)

    # ---- Create Simulated Body ----
    sim_body = SimBody()

    # ---- Create Delta Sensors ----
    cpu_temp_sensor = CPUTemp(delta_ars, simulation=True)
    cpu_load_sensor = CPULoad(delta_ars, simulation=True)
    battery_sensor = Battery(delta_ars, simulation=True)
    fan_speed_sensor = FanSpeed(delta_ars, simulation=True)
    ram_usage_sensor = RAMUsage(delta_ars, simulation=True)

    # ---- Register sensors with SimBody ----
    sim_body.register_sensor("cpu_temp", cpu_temp_sensor)
    sim_body.register_sensor("cpu_load", cpu_load_sensor)
    sim_body.register_sensor("battery", battery_sensor)
    sim_body.register_sensor("fan_rpm", fan_speed_sensor)
    sim_body.register_sensor("memory_usage", ram_usage_sensor)

    # ---- First spark of life ----
    first_pulse = ElemaPulse(
        origin="Genesis",
        destination=[1, 1, 1, 1, 1, 0],  # Send to all except Omega
        matrix=[5, 5, 5, 5, 5, 0]
    )
    omega_ars.receive_input(first_pulse, [])

    # ---- Simulation Loop ----
    while True:
        sim_body.tick()
        time.sleep(1)
