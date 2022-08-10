import logging    
logging.basicConfig(level=logging.INFO)
from src.adc import Adc
from time import sleep 
import RPi.GPIO as G
G.setwarnings(False)
import src.pinnames as pins

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

buttons_pressed = [False, False]

def button_callback(channel) -> None:
    global buttons_pressed
    if channel == pins.SW1:
        logging.info(f"{bcolors.OKBLUE}Button 1 pressed{bcolors.ENDC}")
        G.output(pins.LD1, True)
        buttons_pressed[0] = True
        G.remove_event_detect(pins.SW1)
    else:
        logging.info(f"{bcolors.OKBLUE}Button 2 pressed{bcolors.ENDC}")
        G.output(pins.LD2, True)
        buttons_pressed[1] = True
        G.remove_event_detect(pins.SW2)
    
    if buttons_pressed[0] == True and buttons_pressed[1] == True:
        logging.info(f"{bcolors.OKGREEN}{bcolors.BOLD}Both buttons OK{bcolors.ENDC}\n{bcolors.UNDERLINE}\tVerify that both LEDs are lit{bcolors.ENDC}")
        sleep(3)
        G.output(pins.LD1, False)
        G.output(pins.LD2, False)

def init_user_io() -> None:
    logging.debug("Initiating button inputs and led outputs")
    G.setup([pins.LD1, pins.LD2], G.OUT)
    G.setup([pins.SW1, pins.SW2], G.IN)

    G.add_event_detect(pins.SW1, G.RISING)
    G.add_event_detect(pins.SW2, G.RISING)
    
    G.add_event_callback(pins.SW1, button_callback)
    G.add_event_callback(pins.SW2, button_callback)


def motor_opto_test() -> bool:
    test_result = True
    logging.info("Testing motordriver")

    opt = [pins.OPT1, pins.OPT2, pins.OPT3, pins.OPT4]
    motors = [pins.M2, pins.M1, pins.M4, pins.M3]

    logging.debug("Initialsing motor output pins")
    G.setup(motors, G.OUT)
    logging.debug("Initialsing opto-coupler inputs (with pullup)")
    G.setup(opt, G.IN, pull_up_down=G.PUD_UP)

    for i in range(4):
        logging.debug(f"Testing M{i+1} & OPT1-4")
        G.output(motors, G.LOW)
        
        sleep(0.5)
        G.output(motors[i], G.HIGH)
        
        sleep(1)
        inputs = [G.input(j) for j in opt]
        test = [0 if i == k else 1 for k in range(4)]

        if inputs == test:
            logging.info(f"{bcolors.OKCYAN}M{i+1} & OPT1-4 passed{bcolors.ENDC}")
        else:
            test_result = False
            logging.error(f"{bcolors.FAIL}M{i+1} & OPT1-4 failed{bcolors.ENDC}")
            logging.error(f"{bcolors.FAIL}OPT inputs read: {inputs}, and was supposed to be {test}{bcolors.ENDC}")
            
        sleep(0.5)

    G.output(motors, G.LOW)

    return test_result

def adc_test() -> bool:
    test_result = True
    logging.info("Testing ADC")

    a = Adc()
    for n in range(8):
        reading = a.adc_read_singleended(n)
        logging.info(f"{bcolors.OKCYAN}Ch{n}: {reading:4}: {Adc.convert_reading_to_voltage(reading, 5):4} V{bcolors.ENDC}")
        if n == 0 and reading < 1000:
            test_result = False
            logging.error(f"{bcolors.FAIL}ADC test failed. Channel {n} reading to low.{bcolors.ENDC}")
        if n > 0 and n != 5 and reading > 50:
            test_result = False
            logging.error(f"{bcolors.FAIL}ADC test failed. Channel {n} reading to high.{bcolors.ENDC}")
    
    return test_result


if __name__ == "__main__":
    logging.info(f"{bcolors.BOLD}Running tests...{bcolors.ENDC}\n")

    init_user_io()

    if adc_result := adc_test():
        logging.info(f"{bcolors.OKGREEN}{bcolors.BOLD}ADC test passed{bcolors.ENDC}\n")
    if motor_result := motor_opto_test():
        logging.info(f"{bcolors.OKGREEN}{bcolors.BOLD}Motordriver test passed{bcolors.ENDC}\n")

    if adc_result and motor_result and buttons_pressed[0] and buttons_pressed[1]:
        logging.info(f"{bcolors.OKGREEN}{bcolors.BOLD}All tests passed{bcolors.ENDC}")
    else:
        logging.warning(f"{bcolors.WARNING}{bcolors.BOLD}One or more tests failed{bcolors.ENDC}")
