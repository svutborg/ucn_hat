from src.adc import Adc
from time import sleep

analog = Adc()

class Joystick:

    def __init__(self, x_channel: int, y_channel: int):
        self.adc = Adc()
        self.x_channel = x_channel
        self.y_channel = y_channel
        self.x_bias = 512
        self.y_bias = 512

    def read_axis(self, axis: str) -> int:
        if axis in "xX":
            self.x = self.adc.adc_read_singleended(self.x_channel)
            return self.x
        if axis in "yY":
            self.y = self.adc.adc_read_singleended(self.y_channel)
            return self.y

    def get_vector(self) -> tuple[float]:
        result = (0.0, 0.0)
        x = self.read_axis("x")
        y = self.read_axis("y")
        result = ((x-self.x_bias)/512, (y-self.y_bias)/512)
        return result

    def calibrate_bias(self, number_of_samples: int = 10) -> None:
        x = 0
        y = 0
        for i in range(number_of_samples):
            x += self.read_axis("x")
            y += self.read_axis("y")
        self.x_bias = x/number_of_samples
        self.y_bias = y/number_of_samples


if __name__ == "__main__":
    j = Joystick(3, 2)
    j.calibrate_bias()
    
    while True:
        print(j.get_vector())
        sleep(0.1)