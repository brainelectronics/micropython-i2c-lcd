#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Very simple blink helper module

Toggle given pin on and off with some delay
"""

from time import sleep


def flash_led(pin, amount, on_time=0.5, off_time=0.5):
    """
    Flash onboard LED at given pin

    :param      pin:       The pin connected to the LED
    :type       pin:       int
    :param      amount:    The amount the LED flashes
    :type       amount:    int
    :param      on_time:   On time of the LED
    :type       on_time:   Union[float, int]
    :param      off_time:  Off time of the LED
    :type       off_time:  Union[float, int]
    """
    initial_state = pin.value()

    for x in range(1, amount + 1):
        pin.value(1)
        sleep(on_time)
        pin.value(0)
        sleep(off_time)

    pin.value(initial_state)
