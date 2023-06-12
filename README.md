# MicroPython I2C LCD

[![Downloads](https://pepy.tech/badge/micropython-i2c-lcd)](https://pepy.tech/project/micropython-i2c-lcd)
![Release](https://img.shields.io/github/v/release/brainelectronics/micropython-i2c-lcd?include_prereleases&color=success)
![MicroPython](https://img.shields.io/badge/micropython-Ok-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/github/brainelectronics/micropython-i2c-lcd/branch/main/graph/badge.svg)](https://app.codecov.io/github/brainelectronics/micropython-i2c-lcd)
[![CI](https://github.com/brainelectronics/micropython-i2c-lcd/actions/workflows/release.yml/badge.svg)](https://github.com/brainelectronics/micropython-i2c-lcd/actions/workflows/release.yml)

MicroPython package to control HD44780 LCD displays 1602 and 2004 via I2C

---------------

## General

MicroPython package to control HD44780 LCD displays 1602 and 2004 via I2C

📚 The latest documentation is available at
[MicroPython I2C LCD ReadTheDocs][ref-rtd-micropython-i2c-lcd] 📚

<!-- MarkdownTOC -->

- [Installation](#installation)
	- [Install required tools](#install-required-tools)
- [Setup](#setup)
	- [Install package with upip](#install-package-with-upip)
		- [General](#general)
		- [Specific version](#specific-version)
		- [Test version](#test-version)
	- [Manually](#manually)
		- [Upload files to board](#upload-files-to-board)
- [Usage](#usage)
- [Credits](#credits)

<!-- /MarkdownTOC -->

## Installation

### Install required tools

Python3 must be installed on your system. Check the current Python version
with the following command

```bash
python --version
python3 --version
```

Depending on which command `Python 3.x.y` (with x.y as some numbers) is
returned, use that command to proceed.

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Setup

### Install package with upip

Connect the MicroPython device to a network (if possible)

```python
import network
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect('SSID', 'PASSWORD')
station.isconnected()
```

#### General

Install the latest package version of this lib on the MicroPython device

```python
import mip
mip.install("github:brainelectronics/micropython-i2c-lcd")
```

For MicroPython versions below 1.19.1 use the `upip` package instead of `mip`

```python
import upip
upip.install('micropython-i2c-lcd')
```

#### Specific version

Install a specific, fixed package version of this lib on the MicroPython device

```python
import mip
# install a verions of a specific branch
mip.install("github:brainelectronics/micropython-i2c-lcd", version="feature/initial-implementation")
# install a tag version
mip.install("github:brainelectronics/micropython-i2c-lcd", version="0.1.0")
```

For MicroPython versions below 1.19.1 use the `upip` package instead of `mip`

```python
import upip
upip.install('micropython-i2c-lcd==0.1.0')
```

#### Test version

Install a specific release candidate version uploaded to
[Test Python Package Index](https://test.pypi.org/) on every PR on the
MicroPython device. If no specific version is set, the latest stable version
will be used.

```python
import mip
mip.install("github:brainelectronics/micropython-i2c-lcd", version="0.1.0-rc3.dev1")
```

For MicroPython versions below 1.19.1 use the `upip` package instead of `mip`

```python
import upip
# overwrite index_urls to only take artifacts from test.pypi.org
upip.index_urls = ['https://test.pypi.org/pypi']
upip.install('micropython-i2c-lcd==0.1.0rc3.dev1')
```

### Manually

#### Upload files to board

Copy the module to the MicroPython board and import them as shown below
using [Remote MicroPython shell][ref-remote-upy-shell]

Open the remote shell with the following command. Additionally use `-b 115200`
in case no CP210x is used but a CH34x.

```bash
rshell --port /dev/tty.SLAB_USBtoUART --editor nano
```

Perform the following command inside the `rshell` to copy all files and
folders to the device

```bash
mkdir /pyboard/lib
mkdir /pyboard/lib/lcd_i2c

cp lcd_i2c/* /pyboard/lib/lcd_i2c

cp examples/main.py /pyboard
cp examples/boot.py /pyboard
```

## Usage

```python
from lcd_i2c import LCD
from machine import I2C, Pin

# PCF8574 on 0x50
I2C_ADDR = 0x27     # DEC 39, HEX 0x27
NUM_ROWS = 2
NUM_COLS = 16

# define custom I2C interface, default is 'I2C(0)'
# check the docs of your device for further details and pin infos
i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=800000)
lcd = LCD(addr=I2C_ADDR, cols=NUM_COLS, rows=NUM_ROWS, i2c=i2c)

lcd.begin()
lcd.print("Hello World")
```

For further examples check the `examples` folder or the Example chapter in the
docs.

## Credits

Based on [Frank de Brabanders Arduino LiquidCrystal I2C Library][ref-arduino-lcd-i2c-library].

<!-- Links -->
[ref-rtd-micropython-i2c-lcd]: https://micropython-i2c-lcd.readthedocs.io/en/latest/
[ref-remote-upy-shell]: https://github.com/dhylands/rshell
[ref-arduino-lcd-i2c-library]: https://github.com/fdebrabander/Arduino-LiquidCrystal-I2C-library
[ref-test-pypi]: https://test.pypi.org/
[ref-pypi]: https://pypi.org/
