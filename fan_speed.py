from chema import ChemaPacket
from elema import ElemaPulse

class FanSpeed:
    def __init__(self, ars, sim_body):
        self.ars = ars
        self.sim_body = sim_body
        self.last_rpm = None

    def receive_pulse(self, pulse: ElemaPulse):
        fan_rpm = self.sim_body.get_fan_rpm()
        if fan_rpm is not None:
            if self.last_rpm is None or abs(fan_rpm - self.last_rpm) > 200:
                self.last_rpm = fan_rpm
                if fan_rpm > 5000:
                    chema = ChemaPacket(
                        origin="FanSpeed",
                        destination=[1, 0, 0, 0, 0, 0],
                        matrix=[1, 0, 0, 0, 0, 0],
                        tag="stress"
                    )
                    pulse = ElemaPulse(
                        origin="FanSpeed",
                        destination=[1, 0, 0, 0, 0, 0],
                        matrix=[10, 0, 0, 0, 0, 0]
                    )
                    self.ars.receive_input(pulse, [chema])
