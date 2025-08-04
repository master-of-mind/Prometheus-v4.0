from chema import ChemaPacket
from elema import ElemaPulse
import psutil
from laptop_body import LaptopBody

class RAMUsage:
    def __init__(self, ars, simulation=False):
        self.ars = ars
        self.simulation = simulation
        self.last_usage = None
        self.sim_body = LaptopBody() if simulation else None

    def receive_pulse(self, pulse: ElemaPulse):
        if self.simulation:
            usage = self.sim_body.get_memory_usage()
        else:
            usage = psutil.virtual_memory().percent

        if self.last_usage is None or abs(usage - self.last_usage) > 5:
            self.last_usage = usage
            if usage > 90:  # arbitrary high usage warning
                chema = ChemaPacket(
                    origin="RAMUsage",
                    destination=[1, 0, 0, 0, 0, 0],
                    matrix=[1, 0, 0, 0, 0, 0],
                    tag="memory_pressure"
                )
                pulse = ElemaPulse(
                    origin="RAMUsage",
                    destination=[1, 0, 0, 0, 0, 0],
                    matrix=[12, 0, 0, 0, 0, 0]
                )
                self.ars.receive_input(pulse, [chema])
