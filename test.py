import logging
logging.basicConfig(level=logging.INFO)

logging.info("Logging started")

import RPi.GPIO as G
from time import sleep

G.setmode(G.BCM)

import src.pinnames as pins

G.setup([pins.OPT1, pins.OPT2, pins.OPT3, pins.OPT4], G.IN, pull_up_down=G.PUD_UP)

while True:
    print(f"OPT1: {G.input(pins.OPT1)}, OPT2: {G.input(pins.OPT2)}, OPT3: {G.input(pins.OPT3)}, OPT4: {G.input(pins.OPT4)}")
    sleep(0.5)