from chema import ChemaPacket
from elema import ElemaPulse
import psutil
from laptop_body import LaptopBody

class Battery:
    def __init__(self, ars, simulation=False):
        self.ars = ars
        self.simulation = simulation
        self.sim_body = LaptopBody() if simulation else None

    def receive_pulse(self, pulse: ElemaPulse):
        if self.simulation:
            battery = self.sim_body.get_battery()
        else:
            batt_info = psutil.sensors_battery()
            battery = batt_info.percent if batt_info else None

        if battery is not None and battery < 20:
            chema = ChemaPacket(
                origin="Battery",
                destination=[1, 0, 0, 0, 0, 0],
                matrix=[1, 0, 0, 0, 0, 0],
                tag="fear"
            )
            pulse = ElemaPulse(
                origin="Battery",
                destination=[1, 0, 0, 0, 0, 0],
                matrix=[30, 0, 0, 0, 0, 0]
            )
            self.ars.receive_input(pulse, [chema])
