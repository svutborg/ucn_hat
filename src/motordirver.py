import RPi.GPIO as G 
from dataclasses import dataclass
from abc import ABC
import logging
from time import sleep, time

@dataclass
class Ports():
    M1 = {"BCM": 16, "BOARD": 36}
    M2 = {"BCM": 20, "BOARD": 38}
    M3 = {"BCM": 26, "BOARD": 37}
    M4 = {"BCM": 21, "BOARD": 40}
    
    OPT1 = {"BCM": 12, "BOARD": 32}
    OPT2 = {"BCM": 13, "BOARD": 33}
    OPT3 = {"BCM": 18, "BOARD": 12}
    OPT4 = {"BCM": 19, "BOARD": 35}

    pinmodes = {G.BCM: "BCM", G.BOARD: "BOARD"}

    def get_pinmode() -> int:
        pinmode = G.getmode()
        if pinmode == None:
            logging.warning("RPi pinmode not set. Setting to BCM mode.")
            G.setmode(G.BCM)
            pinmode = G.BCM
        return pinmode

    def resolve_pin(port: dict) -> int:
        
        pinmode = Ports.get_pinmode()
        
        port_key = Ports.pinmodes[pinmode]
        return port[port_key]

class Tachometer():

    def __init__(self, port_a: dict, port_b: dict):
        self.count = 0

        self.a = Ports.resolve_pin(port_a)
        self.b = Ports.resolve_pin(port_b)
    
        G.setup([self.a, self.b], G.IN, pull_up_down = G.PUD_UP)
        G.add_event_detect(self.a, G.RISING, callback=self.__tick)

    def __tick(self, channel):
        if G.input(self.b) == G.HIGH:
            self.count = self.count + 1
        else:
            self.count = self.count - 1

    def get_count(self):
        return self.count

    def reset_count(self):
        self.count = 0


class Motor(ABC):

    def __init__(self, port_a: dict, port_b: dict):
        a = Ports.resolve_pin(port_a)
        b = Ports.resolve_pin(port_b)
        G.setup([a, b], G.OUT)
        self.a = G.PWM(a, 50)
        self.b = G.PWM(b, 50)
        self.a.start(0)
        self.b.start(0)


class Brushed_DC_motor(Motor):

    __tach: Tachometer = None
    __ki: float
    __kd: float
    __kp: float
    __windup_limit: float
    __deadzone_compensation: float

    def __init__(self, port_a: dict, port_b: dict, kp:float = 0.2, ki: float = 0, kd: float = 0, windup_limit: float = 30, deadzone_compensation: float = 12):
        super().__init__(port_a, port_b)
        self.__kp = kp # proportional control factor
        self.__ki = ki # integral control factor
        self.__kd = kd # differential control factor
        self.__windup_limit = windup_limit # limit for integral term wind up
        self.__deadzone_compensation = deadzone_compensation
        
    def attach_tachometer(self, tach: Tachometer):
        self.__tach = tach

    def detach_tachometer(self):
        self.__tach = None
    
    def get_tachometer_count(self):
        return self.__tach.get_count()

    def set_speed(self, speed: int):
        if speed > 100:
            speed = 100
        if speed < -100:
            speed = -100
        if speed > 0:
            self.a.ChangeDutyCycle(speed)
            self.b.ChangeDutyCycle(0)
        else:
            self.b.ChangeDutyCycle(-speed)
            self.a.ChangeDutyCycle(0)
    
    def set_distance(self, distance: int, speed: int = 100):
        target = self.get_tachometer_count() + distance
        error = distance
        last_error = error
        integral = 0
        t1 = time()
        try:
            while not ((-1 < error < 1) ):# and (-5 < integral < 5)):
                logging.info(f"Calculated error signal: {error}")
                t2 = t1
                t1 = time()
                td = t1-t2
                differential = (error - last_error)/td

                integral = integral + error*td
                logging.info(f"Calculated integral signal: {integral}")
                
                # anti-windup
                if integral < -self.__windup_limit:
                    integral = -self.__windup_limit
                if integral > self.__windup_limit:
                    integral = self.__windup_limit

                logging.info(f"Limited integral signal: {integral}")
                
                control = self.__kp * error + self.__ki * integral + self.__kd * differential
                if error > 0:
                    control = control + self.__deadzone_compensation
                else:
                    control = control - self.__deadzone_compensation

                logging.info(f"Calculated control signal: {control}")
                self.set_speed(control)

                last_error = error
                error = target - self.get_tachometer_count()
                sleep(0.01)
        
            self.set_speed(0)
        except TypeError:
            raise AssertionError("Motor must have tachometer attached to run distance")


class Motordirver():

    def __init__(self, motors: list[Motor]):
        self.motors = motors
    
    def forward(self, distance: int = None):
        for m in self.motors:
            if distance == None:
                m.set_speed(100)
            else:
                m.set_distance(distance)
    
    def backward(self, distance: int = None):
        for m in self.motors:
            if distance == None:
                m.set_speed(-100)
            else:
                m.set_distance(distance)

    def stop(self):
        for m in self.motors:
            m.set_speed(0)
