#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest for MicroPython Package template"""

import logging
from nose2.tools import params
import sys
from typing import Optional, Union
import unittest

# custom imports
from be_upy_blink import flash_led


class Pin(object):
    """Fake MicroPython Pin class"""
    IN = 1
    OUT = 2

    def __init__(self, pin: int, mode: int):
        self._pin = pin
        self._mode = mode
        self._value = 0

    def value(self, val: Optional[Union[int, bool]] = None) -> Optional[int]:
        if val is None:
            return self._value
        else:
            self._value = val


class TestBlink(unittest.TestCase):
    """This class describes a TestBlink unittest."""

    def setUp(self) -> None:
        """Run before every test method"""
        # define a format
        custom_format = "[%(asctime)s][%(levelname)-8s][%(filename)-20s @" \
                        " %(funcName)-15s:%(lineno)4s] %(message)s"

        # set basic config and level for all loggers
        logging.basicConfig(level=logging.INFO,
                            format=custom_format,
                            stream=sys.stdout)

        # create a logger for this TestSuite
        self.test_logger = logging.getLogger(__name__)

        # set the test logger level
        self.test_logger.setLevel(logging.DEBUG)

        # enable/disable the log output of the device logger for the tests
        # if enabled log data inside this test will be printed
        self.test_logger.disabled = False

    @params(
        (1),    # set pin initially HIGH
        (0),    # set pin initially LOW
    )
    def test_flash_led(self, init_state: int) -> None:
        """Test flashing of LED with fake Pin"""
        led_pin = Pin(4, Pin.OUT)
        led_pin.value(init_state)
        initial_state = led_pin.value()
        assert init_state == initial_state, "Pin not in specified init_state"

        flash_led(pin=led_pin, amount=3)

        self.assertEqual(initial_state, led_pin.value())

    def tearDown(self) -> None:
        """Run after every test method"""
        pass


if __name__ == '__main__':
    unittest.main()
