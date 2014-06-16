##
# Ultrasonic library for MicroPython's pyboard.
# Compatible with HC-SR04 and SRF04.
#
# Copyright 2014 - Sergio Conde Gómez <skgsergio@gmail.com> 
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

import pyb

# Pin configuration.
# WARNING: Do not use PA4-X5 or PA5-X6 as the echo pin without a 1k resistor.
triggerPin = pyb.Pin.board.X3
echoPin = pyb.Pin.board.X4

# Init trigger pin (out)
trigger = pyb.Pin(triggerPin)
trigger.init(pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
trigger.low()

# Init echo pin (in)
echo = pyb.Pin(echoPin)
echo.init(pyb.Pin.IN, pyb.Pin.PULL_NONE)

def calcDist():
    start = 0
    end = 0

    # Create a microseconds counter.
    micros = pyb.Timer(2, prescaler=83, period=0x3fffffff)
    micros.counter(0)

    # Send a 10us pulse.
    trigger.high()
    pyb.udelay(10)
    trigger.low()

    # Wait 'till whe pulse starts.
    while echo.value() == 0:
        start = micros.counter()

    # Wait 'till the pulse is gone.
    while echo.value() == 1:
        end = micros.counter()

    # Deinit the microseconds counter
    micros.deinit()

    # Calc the duration of the recieved pulse, divide the result by 2 (round-trip)
    # and divide it by 29 (the speed of sound is 340 m/s and that is 29 us/cm).
    return ((end - start) / 2) / 29
