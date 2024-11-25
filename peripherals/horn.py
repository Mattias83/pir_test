import threading
from time import sleep

import RPi.GPIO as GPIO

class Horn:
    horn_pin = 38
    def __init__(self, signal_length: int, signal_delay: int, repetions: int) -> None:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.horn_pin, GPIO.OUT)
        self.signal_length = signal_length
        self.signal_delay = signal_delay
        self.repetions = repetions
        self._stop_event = threading.Event()
        
    def short(self) -> None:
        GPIO.output(self.horn_pin, GPIO.HIGH)
        sleep(55/1000)
        GPIO.output(self.horn_pin, GPIO.LOW)

    def activate(self) -> None:
        self._start_alarm()

    def deactivate(self) -> None:
        self._stop_alarm()

    def _alarm(self) -> None:
        reps: int = self.repetions
        while not self._stop_event.is_set():
            GPIO.output(self.horn_pin, GPIO.HIGH)
            sleep(self.signal_length/1000)
            GPIO.output(self.horn_pin, GPIO.LOW)
            sleep(self.signal_length/1000)
            reps -= 1
            if reps <= 0:
                self._stop_alarm()

    def _start_alarm(self) -> None:
        if not hasattr(self, "_thread") or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._alarm)
            self._thread.start()
    
    def _stop_alarm(self) -> None:
        self._stop_event.set()
        if hasattr(self, "_thread"):
            self._thread.join()