from chema import ChemaPacket
from elema import ElemaPulse
import psutil
from laptop_body import LaptopBody

class CPULoad:
    def __init__(self, ars, simulation=False):
        self.ars = ars
        self.simulation = simulation
        self.last_load = None
        self.sim_body = LaptopBody() if simulation else None

    def receive_pulse(self, pulse: ElemaPulse):
        if self.simulation:
            load = self.sim_body.get_cpu_load()
        else:
            load = psutil.cpu_percent()

        if self.last_load is None or abs(load - self.last_load) > 10:
            self.last_load = load
            if load > 85:
                chema = ChemaPacket(
                    origin="CPULoad",
                    destination=[1, 0, 0, 0, 0, 0],
                    matrix=[1, 0, 0, 0, 0, 0],
                    tag="load"
                )
                pulse = ElemaPulse(
                    origin="CPULoad",
                    destination=[1, 0, 0, 0, 0, 0],
                    matrix=[15, 0, 0, 0, 0, 0]
                )
                self.ars.receive_input(pulse, [chema])
