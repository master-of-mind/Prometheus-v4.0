from chema import ChemaPacket
from elema import ElemaPulse
import psutil
from laptop_body import LaptopBody

class CPUTemp:
    def __init__(self, ars, simulation=False):
        self.ars = ars
        self.simulation = simulation
        self.last_temp = None
        self.sim_body = LaptopBody() if simulation else None

    def receive_pulse(self, pulse: ElemaPulse):
        if self.simulation:
            cpu_temp = self.sim_body.get_cpu_temp()
        else:
            temps = psutil.sensors_temperatures()
            cpu_temp = temps.get('coretemp', [])[0].current if 'coretemp' in temps else None

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
