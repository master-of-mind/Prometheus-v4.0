from chema import ChemaPacket
from elema import ElemaPulse
import psutil
from laptop_body import LaptopBody

class FanSpeed:
    def __init__(self, ars, simulation=False):
        self.ars = ars
        self.simulation = simulation
        self.last_rpm = None
        self.sim_body = LaptopBody() if simulation else None

    def receive_pulse(self, pulse: ElemaPulse):
        if self.simulation:
            fan_rpm = self.sim_body.get_fan_rpm()
        else:
            temps = psutil.sensors_fans()
            if temps:
                first_sensor = list(temps.keys())[0]
                fan_rpm = temps[first_sensor][0].current
            else:
                fan_rpm = None

        if fan_rpm is not None:
            if self.last_rpm is None or abs(fan_rpm - self.last_rpm) > 200:
                self.last_rpm = fan_rpm
                if fan_rpm > 5000:  # arbitrary high RPM warning
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
