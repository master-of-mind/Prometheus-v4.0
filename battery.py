from chema import ChemaPacket
from elema import ElemaPulse

class Battery:
    def __init__(self, ars, sim_body):
        self.ars = ars
        self.sim_body = sim_body

    def receive_pulse(self, pulse: ElemaPulse):
        battery = self.sim_body.get_battery()
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
