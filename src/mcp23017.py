from smbus2 import SMBus

class Mcp23017():
    
    IODIRA =   0x00
    IODIRB =   0x01
    IPOLA =    0x02
    IPOLB =    0x03
    GPINTENA = 0x04
    GPINTENB = 0x05
    DEFVALA =  0x06
    DEFVALB =  0x07
    INTCONA =  0x08
    INTCONB =  0x09
    IOCONA =   0x0A
    IOCONB =   0x0B
    GPPUA =    0x0C
    GPPUB =    0x0D
    INTFA =    0x0E
    INTFB =    0x0F
    INTCAPA =  0x10
    INTCAPB =  0x11
    GPIOA =    0x12
    GPIOB =    0x13
    OLATA =    0x14
    OLATB =    0x15

    def __init__(self, address: int = 0) -> None:
        self.address = 0b0100000 | address # [0 1 0 0 A2 A1 A0]
        self.bus = SMBus(1)

    def write_register(self, register, data):
        self.bus.write_byte_data(self.address, register, data)

    def read_register(self, register):
        return self.bus.read_byte_data(self.address, register)


if __name__ == "__main__":
    pass