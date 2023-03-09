# MicroPython package template

[![Downloads](https://pepy.tech/badge/micropython-package-template)](https://pepy.tech/project/micropython-package-template)
![Release](https://img.shields.io/github/v/release/brainelectronics/micropython-package-template?include_prereleases&color=success)
![MicroPython](https://img.shields.io/badge/micropython-Ok-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/github/brainelectronics/micropython-package-template/branch/main/graph/badge.svg)](https://app.codecov.io/github/brainelectronics/micropython-package-template)
[![CI](https://github.com/brainelectronics/micropython-package-template/actions/workflows/release.yml/badge.svg)](https://github.com/brainelectronics/micropython-package-template/actions/workflows/release.yml)

MicroPython PyPi package template project with auto deploy

---------------

## General

MicroPython PyPi package template with GitHub Action based testing and deploy

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
- [Create a PyPi \(micropython\) package](#create-a-pypi-micropython-package)
	- [Setup](#setup-1)
	- [Create a distribution](#create-a-distribution)
	- [Upload to PyPi](#upload-to-pypi)
- [Contributing](#contributing)
	- [Unittests](#unittests)
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
station.connect('SSID', 'PASSWORD')
station.isconnected()
```

#### General

Install the latest package version of this lib on the MicroPython device

```python
import upip
upip.install('micropython-package-template')
```

#### Specific version

Install a specific, fixed package version of this lib on the MicroPython device

```python
import upip
upip.install('micropython-package-template==0.1.1')
```

#### Test version

Install a specific release candidate version uploaded to
[Test Python Package Index](https://test.pypi.org/) on every PR on the
MicroPython device. If no specific version is set, the latest stable version
will be used.

```python
import upip
# overwrite index_urls to only take artifacts from test.pypi.org
upip.index_urls = ['https://test.pypi.org/pypi']
upip.install('micropython-package-template==0.2.0rc1.dev6')
```

See also [brainelectronics Test PyPi Server in Docker][ref-brainelectronics-test-pypiserver]
for a test PyPi server running on Docker.

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
mkdir /pyboard/lib/be_upy_blink

cp be_upy_blink/* /pyboard/lib/be_upy_blink

cp examples/main.py /pyboard
cp examples/boot.py /pyboard
```

## Usage

```python
from be_upy_blink import flash_led
from machine import Pin

led_pin = Pin(4, Pin.OUT)

flash_led(pin=led_pin, amount=3)
# flash_led(pin=led_pin, amount=3, on_time=1, off_time=3)
```

## Create a PyPi (micropython) package

### Setup

Install the required python package with the following command in a virtual
environment to avoid any conflicts with other packages installed on your local
system.

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install twine
```

### Create a distribution

This module overrides distutils (also compatible with setuptools) `sdist`
command to perform pre- and post-processing as required for MicroPython's
upip package manager. This script is taken from
[pfalcon's picoweb][ref-pfalcon-picoweb-sdist-upip] and updated to be PEP8
conform.

```bash
python setup.py sdist
```

A new folder `dist` will be created. The [`sdist_upip`](sdist_upip.py) will be
used to create everything necessary.

### Upload to PyPi

**Be aware: [pypi.org][ref-pypi] and [test.pypi.org][ref-test-pypi] are different**

You can **NOT** login to [test.pypi.org][ref-test-pypi] with the
[pypi.org][ref-pypi] account unless you created the same on the other. See
[invalid auth help page of **test** pypi][ref-invalid-auth-test-pypi]

For testing purposes add `--repository testpypi` to
upload it to [test.pypi.org][ref-test-pypi]

```bash
twine upload dist/micropython-package-template-*.tar.gz -u PYPI_USERNAME -p PYPI_PASSWORD
```

## Contributing

### Unittests

Run the unittests locally with the following command after installing this
package in a virtual environment

```bash
# run all tests
nose2 --config tests/unittest.cfg

# run only one specific tests
nose2 tests.test_blink.TestBlink.test_flash_led
```

Generate the coverage files with

```bash
python create_report_dirs.py
coverage html
```

The coverage report is placed at `reports/coverage/html/index.html`

## Credits

Based on the [PyPa sample project][ref-pypa-sample].

<!-- Links -->
[ref-remote-upy-shell]: https://github.com/dhylands/rshell
[ref-brainelectronics-test-pypiserver]: https://github.com/brainelectronics/test-pypiserver
[ref-pypa-sample]: https://github.com/pypa/sampleproject
[ref-pfalcon-picoweb-sdist-upip]: https://github.com/pfalcon/picoweb/blob/b74428ebdde97ed1795338c13a3bdf05d71366a0/sdist_upip.py
[ref-test-pypi]: https://test.pypi.org/
[ref-pypi]: https://pypi.org/
[ref-invalid-auth-test-pypi]: https://test.pypi.org/help/#invalid-auth
