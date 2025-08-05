from chema import ChemaPacket
from elema import ElemaPulse

class RAMUsage:
    def __init__(self, ars, sim_body):
        self.ars = ars
        self.sim_body = sim_body
        self.last_usage = None

    def receive_pulse(self, pulse: ElemaPulse):
        usage = self.sim_body.get_memory_usage()
        if self.last_usage is None or abs(usage - self.last_usage) > 5:
            self.last_usage = usage
            if usage > 90:
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
