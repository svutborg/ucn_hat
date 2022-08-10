import RPi.GPIO as G
import logging

def get_pinmode() -> int:
    pinmode = G.getmode()
    if pinmode == None:
        logging.warning("RPi pinmode not set. Setting to BCM mode.")
        G.setmode(G.BCM)
        pinmode = G.BCM
    return pinmode

if get_pinmode() == G.BCM:

    ## Serial Interfaces:
    # I2C
    I2C_SDA: int = 2
    I2C_SCL: int = 3

    # SPI
    SPI_MOSI: int = 10
    SPI_MISO: int = 9
    SPI_CLK: int = 11
    SPI_CS0: int = 8
    SPI_CS1: int = 9

    # UART
    UART_TX: int = 14
    UART_RX: int = 15


    ## User Input/Output
    # Switches
    SW1: int = 5
    SW2: int = 6
    BTN1: int = SW1
    BTN2: int = SW2

    # Lightemitting diodes
    LD1: int = 23
    LD2: int = 24
    LED1: int = LD1
    LED2: int = LD2

    ## Input/Output
    # Motor outputs
    M1: int = 16
    M2: int = 20
    M3: int = 26
    M4: int = 21

    # Opto-coupler inputs
    OPT1: int = 12
    OPT2: int = 13
    OPT3: int = 18
    OPT4: int = 19
else:

    ## Serial Interfaces:
    # I2C
    I2C_SDA: int = 3
    I2C_SCL: int = 5

    # SPI
    SPI_MOSI: int = 19
    SPI_MISO: int = 21
    SPI_CLK: int = 23
    SPI_CS0: int = 24
    SPI_CS1: int = 26

    # UART
    UART_TX: int = 8
    UART_RX: int = 10


    ## User Input/Output
    # Switches
    SW1: int = 29
    SW2: int = 31
    BTN1: int = SW1
    BTN2: int = SW2

    # Lightemitting diodes
    LD1: int = 16
    LD2: int = 18
    LED1: int = LD1
    LED2: int = LD2

    ## Input/Output
    # Motor outputs
    M1: int = 36
    M2: int = 38
    M3: int = 37
    M4: int = 40

    # Opto-coupler inputs
    OPT1: int = 32
    OPT2: int = 33
    OPT3: int = 12
    OPT4: int = 35