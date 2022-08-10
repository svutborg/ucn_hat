import spidev
from dataclasses import dataclass, fields

class Adc():

    @dataclass
    class Differential_combinations():
        ch0_ch1: int = 0x0
        ch1_ch0: int = 0x1
        ch2_ch3: int = 0x2
        ch3_ch2: int = 0x3
        ch4_ch5: int = 0x4
        ch5_ch4: int = 0x5
        ch6_ch7: int = 0x6
        ch7_ch6: int = 0x7

    def __init__(self, bus: int = 0, device: int = 0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus = bus, device = device)
        self.spi.max_speed_hz = 100000

    def adc_read_singleended(self, channel: int = 0) -> int:
        to_send = [0x01, 0x80 | channel<<4, 0x55]
        to_send = self.spi.xfer2(to_send)
        return ((to_send[1]&0x03)<<8) + to_send[2]

    def adc_read_differential(self, channels: int = Differential_combinations.ch0_ch1) -> int:
        to_send = [0x01, channels<<4, 0x55]
        to_send = self.spi.xfer2(to_send)
        return ((to_send[1]&0x03)<<8) + to_send[2] 

    def convert_reading_to_voltage(reading: int, reference_voltage: float = 3.3, decimal_digits: int = 2) -> float:
        return round((reading*reference_voltage)/1024, decimal_digits)

if __name__ == "__main__":
    a = Adc()
    for n in range(8):
        reading = a.adc_read_singleended(n)
        print(f"Ch{n}: {reading:4}: {Adc.convert_reading_to_voltage(reading, 5):4} V")
    for combination in fields(Adc.Differential_combinations):
        print(f"{combination.name}: {a.adc_read_differential(combination.default):4}")
