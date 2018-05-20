##
# Ultrasonic library for MicroPython's pyboard.
# Compatible with HC-SR04 and SRF04.
#
# Copyright 2018 - Sergio Conde Gómez <skgsergio@gmail.com>
# Copyright 2014 - Mithru Vigneshwara
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

from time import sleep_us
from machine import Pin, time_pulse_us


class MeasurementTimeout(Exception):
    def __init__(self, timeout):
        super().__init__("Measurement timeout, exceeded {} us".format(timeout))


class Ultrasonic(object):
    def __init__(self, trigger_pin, echo_pin, timeout_us=30000):
        # WARNING: Don't use PA4-X5 or PA5-X6 as echo pin without a 1k resistor

        # Default timeout is a bit more than the HC-SR04 max distance (400 cm):
        # 400 cm * 29 us/cm (speed of sound ~340 m/s) * 2 (round-trip)

        self.timeout = timeout_us

        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.off()

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def distance_in_inches(self):
        return (self.distance_in_cm() * 0.3937)

    def distance_in_cm(self):
        # Send a 10us pulse
        self.trigger.on()
        sleep_us(10)
        self.trigger.off()

        # Wait for the pulse and calc its duration
        time_pulse = time_pulse_us(self.echo, 1, self.timeout)

        if time_pulse < 0:
            raise MeasurementTimeout(self.timeout)

        # Divide the duration of the pulse by 2 (round-trip) and then divide it
        # by 29 us/cm (speed of sound = ~340 m/s)
        return (time_pulse / 2) / 29
