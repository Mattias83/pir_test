from time import sleep

import RPi.GPIO as GPIO
import threading


class Lights:
    lights_pin: int = 36

    def __init__(self, pulse=False) -> None:
        self.pulse = pulse
        self._stop_event = threading.Event()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.lights_pin, GPIO.OUT)

    def on(self) -> None:
        if self.pulse:
            self._start_pulse()
        else:
            GPIO.output(self.lights_pin, GPIO.HIGH)

    def off(self) -> None:
        self._stop_pulse()
        GPIO.output(self.lights_pin, GPIO.LOW)

    def _pulse(self) -> None:
        while not self._stop_event.is_set():
            GPIO.output(self.lights_pin, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(self.lights_pin, GPIO.LOW)
            sleep(0.5)

    def _start_pulse(self) -> None:
        if not hasattr(self, "_thread") or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._pulse)
            self._thread.start()

    def _stop_pulse(self) -> None:
        self._stop_event.set()
        if hasattr(self, "_thread"):
            self._thread.join()
