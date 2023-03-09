#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest for MicroPython I2C LCD"""

import logging
from mock import Mock, patch
from nose2.tools import params
import sys
import unittest


class Pin(object):
    """Fake MicroPython Pin class"""
    def __init__(self, pin: int, mode: int = -1):
        self._pin = pin
        self._mode = mode
        self._value = 0


class I2C(object):
    """Fake MicroPython I2C class"""
    def __init__(self, id: int, *, scl: Pin, sda: Pin, freq: int = 400000):
        self._id = id
        self._scl = scl
        self._sda = sda
        self._freq = freq

    def writeto(addr: int, buf: bytearray, stop: bool = True) -> int:
        return 1


# custom imports
sys.modules['machine.I2C'] = I2C
to_be_mocked = [
    'machine',
    'time.sleep_ms', 'time.sleep_us',
]
for module in to_be_mocked:
    sys.modules[module] = Mock()

from lcd_i2c import LCD             # noqa: E402
from lcd_i2c import const as Const  # noqa: E402


class TestLCD(unittest.TestCase):
    """This class describes a TestLCD unittest."""

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

        self.i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=800_000)
        self._calls_counter = 0
        self._tracked_call_data: list = []

    def _tracked_call(self, *args, **kwargs) -> None:
        """Track function calls and the used arguments"""
        self._tracked_call_data.append({'args': args, 'kwargs': kwargs})

    @params(
        (0x27),
        (39),
    )
    def test_addr(self, addr: int) -> None:
        """Test address property"""
        lcd = LCD(addr=addr, cols=16, rows=2, i2c=self.i2c)

        self.assertEqual(lcd.addr, addr)

    @params(
        (16),
        (20),
    )
    def test_cols(self, cols: int) -> None:
        """Test columns property"""
        lcd = LCD(addr=0x27, cols=cols, rows=2, i2c=self.i2c)

        self.assertEqual(lcd.cols, cols)

    @params(
        (1),
        (2),
        (4),
    )
    def test_rows(self, rows: int) -> None:
        """Test rows property"""
        lcd = LCD(addr=0x27, cols=16, rows=rows, i2c=self.i2c)

        self.assertEqual(lcd.rows, rows)

    def test_charsize(self) -> None:
        """Test charsize property"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        self.assertEqual(lcd.charsize, 0)

        lcd = LCD(addr=0x27, cols=16, rows=2, charsize=1, i2c=self.i2c)
        self.assertEqual(lcd.charsize, 1)

    def test_backlightval(self) -> None:
        """Test backlightval property"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)

        # active by default
        self.assertEqual(lcd.backlightval, Const.LCD_BACKLIGHT)
        self.assertTrue(lcd.get_backlight())

        lcd.no_backlight()
        self.assertEqual(lcd.backlightval, Const.LCD_NOBACKLIGHT)
        self.assertFalse(lcd.get_backlight())

        lcd.backlight()
        self.assertEqual(lcd.backlightval, Const.LCD_BACKLIGHT)
        self.assertTrue(lcd.get_backlight())

        lcd.set_backlight(new_val=False)
        self.assertEqual(lcd.backlightval, Const.LCD_NOBACKLIGHT)
        self.assertFalse(lcd.get_backlight())

        lcd.set_backlight(new_val=True)
        self.assertEqual(lcd.backlightval, Const.LCD_BACKLIGHT)
        self.assertTrue(lcd.get_backlight())

    def test_cursor_position(self) -> None:
        """Test cursor position property"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        self.assertEqual(lcd.cursor_position, (0, 0))

        # test valid cursor position
        lcd.cursor_position = (10, 1)
        self.assertEqual(lcd.cursor_position, (10, 1))

        # test invald cursor position (not enough rows)
        lcd.cursor_position = (10, 2)
        self.assertEqual(lcd.cursor_position, (10, 1))

    def test_begin(self) -> None:
        """Test LCD begin"""
        # default I2C interface
        lcd = LCD(addr=0x27, cols=16, rows=2)
        lcd.begin()

        # self.assertEqual(lcd._i2c._id, 0)
        self.assertEqual(lcd._display_function, 0x8)
        self.assertEqual(lcd._display_control, 0x4)
        self.assertEqual(lcd._display_mode, 2)
        self.assertEqual(lcd.cursor_position, (0, 0))

        # double row display
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        lcd.begin()

        # self.assertEqual(lcd._i2c._id, self.i2c._id)
        self.assertEqual(lcd._display_function, 0x8)
        self.assertEqual(lcd._display_control, 0x4)
        self.assertEqual(lcd._display_mode, 2)
        self.assertEqual(lcd.cursor_position, (0, 0))

        # single row display
        lcd = LCD(addr=0x27, cols=16, rows=1, i2c=self.i2c)
        lcd.begin()

        # self.assertEqual(lcd._i2c._id, self.i2c._id)
        self.assertEqual(lcd._display_function, 0x0)
        self.assertEqual(lcd._display_control, 0x4)
        self.assertEqual(lcd._display_mode, 2)
        self.assertEqual(lcd.cursor_position, (0, 0))

        # single row display with different char size
        lcd = LCD(addr=0x27, cols=16, rows=1, charsize=0x1, i2c=self.i2c)
        lcd.begin()

        # self.assertEqual(lcd._i2c._id, self.i2c._id)
        self.assertEqual(lcd._display_function, 0x4)
        self.assertEqual(lcd._display_control, 0x4)
        self.assertEqual(lcd._display_mode, 2)
        self.assertEqual(lcd.cursor_position, (0, 0))

    def test_clear(self) -> None:
        """Test clear display"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        lcd.set_cursor(col=3, row=1)

        lcd.cursor_position = (3, 1)
        lcd.clear()
        lcd.cursor_position = (0, 0)

    def test_home(self) -> None:
        """Test home display"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        lcd.set_cursor(col=3, row=1)

        lcd.cursor_position = (3, 1)
        lcd.home()
        lcd.cursor_position = (0, 0)

    def test_display(self) -> None:
        """Test display on/off functions"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        lcd.begin()
        self.assertEqual(lcd._display_control, 0x4)

        lcd.no_display()
        self.assertEqual(lcd._display_control, 0x0)

        lcd.display()
        self.assertEqual(lcd._display_control, 0x4)

    def test_blink(self) -> None:
        """Test cursor blink on/off functions"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        lcd.begin()
        self.assertEqual(lcd._display_control, 0x4)

        lcd.blink()
        self.assertEqual(lcd._display_control, 0x5)

        lcd.no_blink()
        self.assertEqual(lcd._display_control, 0x4)

        lcd.blink_on()
        self.assertEqual(lcd._display_control, 0x5)

        lcd.blink_off()
        self.assertEqual(lcd._display_control, 0x4)

    def test_cursor(self) -> None:
        """Test cursor on/off functions"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        lcd.begin()
        self.assertEqual(lcd._display_control, 0x4)

        lcd.cursor()
        self.assertEqual(lcd._display_control, 0x6)

        lcd.no_cursor()
        self.assertEqual(lcd._display_control, 0x4)

        lcd.cursor_on()
        self.assertEqual(lcd._display_control, 0x6)

        lcd.cursor_off()
        self.assertEqual(lcd._display_control, 0x4)

        lcd.cursor()
        lcd.blink()
        self.assertEqual(lcd._display_control, 0x7)

        lcd.no_blink()
        self.assertEqual(lcd._display_control, 0x6)

        lcd.no_cursor()
        self.assertEqual(lcd._display_control, 0x4)

    def test_scroll_display_left(self) -> None:
        """Test scrolling test to the left"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        lcd.begin()

        with patch('lcd_i2c.LCD._command', wraps=self._tracked_call):
            lcd.scroll_display_left()

        self.assertEqual(len(self._tracked_call_data), 1)
        self.assertEqual(self._tracked_call_data[0]['kwargs']['value'], 0x18)

    def test_scroll_display_right(self) -> None:
        """Test scrolling test to the right"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        lcd.begin()

        with patch('lcd_i2c.LCD._command', wraps=self._tracked_call):
            lcd.scroll_display_right()

        self.assertEqual(len(self._tracked_call_data), 1)
        self.assertEqual(self._tracked_call_data[0]['kwargs']['value'], 0x1C)

    def test_text_flow(self) -> None:
        """Test setting text flow left to right"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        lcd.begin()
        self.assertEqual(lcd._display_mode, 0x2)

        lcd.right_to_left()
        self.assertEqual(lcd._display_mode, 0x0)

        lcd.left_to_right()
        self.assertEqual(lcd._display_mode, 0x2)

    def test_autoscroll(self) -> None:
        """Test autoscroll function"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        lcd.begin()
        self.assertEqual(lcd._display_mode, 0x2)

        lcd.autoscroll()
        self.assertEqual(lcd._display_mode, 0x3)

        lcd.no_autoscroll()
        self.assertEqual(lcd._display_mode, 0x2)

    def test_create_char(self) -> None:
        """Test creating custom char"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        lcd.begin()

        charmap = [
            0x0,    # 00000
            0x1,    # 00001
            0x3,    # 00011
            0x7,    # 00111
            0xF,    # 01111
            0x1F,   # 11111
            0x4,    # 00100
            0x11,   # 10001
        ]

        with patch('lcd_i2c.LCD._command', wraps=self._tracked_call):
            lcd.create_char(location=0, charmap=charmap)

        self.assertEqual(len(self._tracked_call_data) - 1, len(charmap))

        # command value to set CGRAM address at the given location
        self.assertEqual(self._tracked_call_data.pop(0)['kwargs']['value'], 64)

        # check char map send command content
        for idx, val in enumerate(charmap):
            self.assertEqual(self._tracked_call_data[idx]['kwargs']['value'],
                             val)

    def test_print(self) -> None:
        """Test print on LCD"""
        lcd = LCD(addr=0x27, cols=16, rows=2, i2c=self.i2c)
        lcd.begin()
        self.assertEqual(lcd.cursor_position, (0, 0))

        text = "Hello"

        with patch('lcd_i2c.LCD._command', wraps=self._tracked_call):
            lcd.print(text)

        # called 1x to much
        self.assertEqual(len(self._tracked_call_data) - 1, len(text))
        self.assertEqual(lcd.cursor_position, (0 + len(text), 0))

        for idx, val in enumerate(text):
            self.assertEqual(self._tracked_call_data[idx]['kwargs']['value'],
                             ord(val))

    def tearDown(self) -> None:
        """Run after every test method"""
        pass


if __name__ == '__main__':
    unittest.main()
