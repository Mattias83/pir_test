import RPi.GPIO as GPIO
import sqlite3

from database import Connection


class PirDetector:
    def __init__(
        self, name: str, signal_pin: int, isActive: int, sensitivity: int, pir_id: int
    ) -> None:
        self.name = name
        self.signal_pin = signal_pin
        self.isActive = isActive
        self.sensitivity = sensitivity
        self.pir_id = pir_id


class PirDetectors:
    def __init__(self, connection: Connection) -> None:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.pir_power_pin = 7
        GPIO.setup(self.pir_power_pin, GPIO.OUT)
        self.connection = connection
        self.detectors: list[PirDetector] = []
        self.fetch()

    def fetch(self) -> None:
        with self.connection as cursor:
            cursor.execute("SELECT * FROM pir_detectors")
            detectors: list[sqlite3.Row] = cursor.fetchall()
            try:
                for detector in detectors:
                    pir_detector: PirDetector = PirDetector(
                        name=detector["name"],
                        signal_pin=detector["signal_pin"],
                        isActive=detector["isActive"],
                        sensitivity=detector["sensitivity"],
                        pir_id=detector["pir_id"],
                    )
                    self.detectors.append(pir_detector)
                self._setup_detectors()
            except Exception as err:
                print(f"Kunde inte hämta pirsensorer från databasen: {err}")

    def power_up(self) -> None:
        GPIO.output(self.pir_power_pin, GPIO.HIGH)

    def power_down(self) -> None:
        GPIO.output(self.pir_power_pin, GPIO.LOW)

    def _setup_detectors(self) -> None:
        for detector in self.detectors:
            GPIO.setup(detector.signal_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    @staticmethod
    def signal(signal_pin: int):
        if GPIO.input(signal_pin):
            return True
