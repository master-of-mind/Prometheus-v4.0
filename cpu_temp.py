from chema import ChemaPacket
from elema import ElemaPulse

class CPUTemp:
    def __init__(self, ars, sim_body):
        self.ars = ars
        self.sim_body = sim_body
        self.last_temp = None

    def receive_pulse(self, pulse: ElemaPulse):
        cpu_temp = self.sim_body.get_cpu_temp()
        if cpu_temp is not None:
            if self.last_temp is None or abs(cpu_temp - self.last_temp) > 1:
                self.last_temp = cpu_temp
                if cpu_temp > 85:
                    chema = ChemaPacket(
                        origin="CPUTemp",
                        destination=[1, 0, 0, 0, 0, 0],
                        matrix=[1, 0, 0, 0, 0, 0],
                        tag="heat"
                    )
                    pulse = ElemaPulse(
                        origin="CPUTemp",
                        destination=[1, 0, 0, 0, 0, 0],
                        matrix=[20, 0, 0, 0, 0, 0]
                    )
                    self.ars.receive_input(pulse, [chema])
