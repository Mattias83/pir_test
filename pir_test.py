#!/usr/bin/python3
"""
Testprogram för att kontrollera aktivitet på pirsensorer ansluta till
MachineGuard. Hämtar rörelsedetektorerna från MachineGuard så det blir
lättare att se vilken sensor som ger utslag genom att se namnet på 
sensorn.

Starta utan växlar för att kontrollera alla "aktiva" pirsensorer.
Med aktiv innebär att isActive är True i inställningarna för 
pirsensorn.

Start med -all_detectors för att kontrollera samtliga ansluta pirsensorer

Starta med -lights om du vill att lamporna som är ansluta till MachineGuard
tänds när någon pirsensor ger utslag. 

Skrivit av Mattias Lindberg, Götalands Maskinservice AB. mattias@gmsmaskin.se
"""

from datetime import datetime
from time import sleep
import sys
import os

from database import Connection
from pir_detectors import PirDetectors
from pir_detectors import PirDetector
from peripherals import Lights

from cli_parser import CliParser, Argument

# Setup command line arguments
use_all_detectors = Argument("-all_detectors")
use_lights_with_detection = Argument("-lights")
pulse_lights = Argument("-pulse")
cli_parser = CliParser([use_all_detectors, use_lights_with_detection])

# Get pir detectors from database, PirDetectors class setups alla detectors
# for easy use. Use staticmethod signal from PirDetectors to check for
# activity.
db_location = os.getenv("MACHINEGUARD_DB", "")
pir_detectors = PirDetectors(Connection(db_location))
detectors: list[PirDetector] = pir_detectors.detectors

ALL_DETECTORS: bool = False
USE_LIGHTS: bool = False
PULSE_LIGHTS: bool = False

# Initialize lighs module, use .on() or .off(). Set pulse=True for
# pulseing lights. See peripherals package for more details...
lights = Lights(pulse=PULSE_LIGHTS)


def main() -> None:
    if ALL_DETECTORS:
        print("Läser av samtliga rörelsedetektorer")
    else:
        print("Läser endast av aktiva rörelsedetektorer")

    if USE_LIGHTS:
        print("Tänder lamporna vid utslag")
    else:
        print("Visar endast utslag i terminalen")

    print("Startar upp pirsensorer")
    pir_detectors.power_up()
    sleep(3)
    print("Pirsensorer aktiva")

    print("Starta scriptet med följande välxar")
    print(" -all_detectors för att läsa av samtliga rörelsedetektorer")
    print(" -lights för att tänd lamporna vid utslag på rörelsedetektor")
    print("")
    print("Vi startar loopen nu, avbryt med CTRL-C")
    try:
        while True:
            sleep(1)  # delay one second per loop cykle
            if USE_LIGHTS:
                lights.off()
            now = datetime.now().strftime("%Y-%M-%D %H:%M:%S")
            for detector in detectors:
                if detector.isActive or ALL_DETECTORS:
                    if PirDetectors.signal(detector.signal_pin):
                        print(f"{now} : Utslag {detector.name}")
                        if USE_LIGHTS:
                            print("lampa tänds")
                            lights.on()
    except KeyboardInterrupt:
        pir_detectors.power_down()
        lights.off()
        print("\nStänger av strömmen till rörelsedetektorerna och stänger av")


if __name__ == "__main__":
    cli_parser.parse(sys.argv)
    if cli_parser.check("-all_detectors"):
        ALL_DETECTORS = True
    if cli_parser.check("-lights"):
        USE_LIGHTS = True
    if cli_parser.check("-pulse"):
        PULSE_LIGHTS = True

    main()
