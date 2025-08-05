from chema import ChemaPacket
from elema import ElemaPulse

class CPULoad:
    def __init__(self, ars, sim_body):
        self.ars = ars
        self.sim_body = sim_body
        self.last_load = None

    def receive_pulse(self, pulse: ElemaPulse):
        load = self.sim_body.get_cpu_load()
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
