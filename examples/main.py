#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""I2C LCD showcase"""

from lcd_i2c import LCD
from machine import I2C, Pin
from time import sleep

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
FREQ = 800000   # Try lowering this value in case of "Errno 5"


def print_and_wait(text: str, sleep_time: int = 2) -> None:
    """
    Print to console and wait some time.

    :param      text:        The text to print to console
    :type       text:        str
    :param      sleep_time:  The sleep time in seconds
    :type       sleep_time:  int
    """
    print(text)
    sleep(sleep_time)


# define custom I2C interface, default is 'I2C(0)'
# check the docs of your device for further details and pin infos
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=FREQ)
lcd = LCD(addr=I2C_ADDR, cols=I2C_NUM_COLS, rows=I2C_NUM_ROWS, i2c=i2c)

# get LCD infos/properties
print("LCD is on I2C address {}".format(lcd.addr))
print("LCD has {} columns and {} rows".format(lcd.cols, lcd.rows))
print("LCD is used with a charsize of {}".format(lcd.charsize))
print("Cursor position is {}".format(lcd.cursor_position))

# start LCD, not automatically called during init to be Arduino compatible
lcd.begin()

# print text on sceen at first row, starting on first column
lcd.print("Hello World")
print_and_wait("Show 'Hello World' on LCD")

# turn LCD off
lcd.no_backlight()
print_and_wait("Turn LCD backlight off")

# get current backlight value
print_and_wait("Backlight value: {}".format(lcd.get_backlight()))

# turn LCD on
lcd.backlight()
print_and_wait("Turn LCD backlight on")

# get current backlight value
print_and_wait("Backlight value: {}".format(lcd.get_backlight()))

# clear LCD display content
lcd.clear()
print_and_wait("Clear display content")

# turn cursor on (show)
lcd.cursor()
print_and_wait("Turn cursor on (show)")

# blink cursor
lcd.blink()
print_and_wait("Blink cursor")

# return cursor to home position
lcd.home()
print_and_wait("Return cursor to home position")

# stop blinking cursor
lcd.no_blink()
print_and_wait("Stop blinking cursor")

# turn cursor off (hide)
lcd.no_cursor()
print_and_wait("Turn cursor off (hide)")

# print_and_wait text on sceen
lcd.print("Hello again")
print_and_wait("Show 'Hello again' on LCD")

# turn display off
lcd.no_display()
print_and_wait("Turn LCD off")

# turn display on
lcd.display()
print_and_wait("Turn LCD on")

# scroll display to the left
for _ in "Hello again":
    lcd.scroll_display_left()
    sleep(0.5)
print_and_wait("Scroll display to the left")

# scroll display to the right
for _ in "Hello again":
    lcd.scroll_display_right()
    sleep(0.5)
print_and_wait("Scroll display to the right")

# set text flow right to left
lcd.clear()
lcd.right_to_left()
lcd.print("Right to left")
print_and_wait("Set text flow right to left")

# set text flow left to right
lcd.left_to_right()
lcd.clear()
lcd.print("Left to right")
print_and_wait("Set text flow left to right")

# activate autoscroll
lcd.autoscroll()
print_and_wait("Activate autoscroll")

# disable autoscroll
lcd.no_autoscroll()
print_and_wait("Disable autoscroll")

# set cursor to second line, seventh column
lcd.clear()
lcd.cursor()
# lcd.cursor_position = (7, 1)
lcd.set_cursor(col=7, row=1)
print_and_wait("Set cursor to row 1, column 7")
lcd.no_cursor()

# set custom char number 0 as :-)
# custom char can be set for location 0 ... 7
lcd.create_char(
    location=0,
    charmap=[0x00, 0x00, 0x11, 0x04, 0x04, 0x11, 0x0E, 0x00]
    # this is the binary matrix, feel it, see it
    # 00000
    # 00000
    # 10001
    # 00100
    # 00100
    # 10001
    # 01110
    # 00000
)
print_and_wait("Create custom char ':-)'")

# show custom char stored at location 0
lcd.print(chr(0))
print_and_wait("Show custom char")
