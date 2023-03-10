#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup
from pathlib import Path
import sdist_upip

here = Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# load elements of version.py
exec(open(here / 'lcd_i2c' / 'version.py').read())

setup(
    name='micropython-i2c-lcd',
    version=__version__,
    description="Micropython package to control HD44780 LCD displays 1602 and 2004 ",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/brainelectronics/micropython-i2c-lcd',
    author='brainelectronics',
    author_email='info@brainelectronics.de',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='micropython, HD44780, I2C, display, LCD1602, LCD2004',
    project_urls={
        'Bug Reports': 'https://github.com/brainelectronics/micropython-i2c-lcd/issues',
        'Source': 'https://github.com/brainelectronics/micropython-i2c-lcd',
    },
    license='MIT',
    cmdclass={'sdist': sdist_upip.sdist},
    packages=['lcd_i2c'],
    install_requires=[]
)
