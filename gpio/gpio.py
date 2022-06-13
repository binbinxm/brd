#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
read i2c eeprom, m24m02
"""

#pylint: disable-msg=broad-except
#pylint: disable-msg=too-few-public-methods

from time import sleep
import traceback

from prompt_toolkit import prompt

from argparse import ArgumentParser, FileType
from logging import Formatter, StreamHandler, getLogger, DEBUG, ERROR
from sys import modules, stderr
from traceback import format_exc
from pyftdi import FtdiLogger
from pyftdi.ftdi import Ftdi
from pyftdi.i2c import I2cController, I2cNackError
from pyftdi.misc import add_custom_devices
from pyftdi.gpio import (GpioAsyncController,
                         GpioSyncController,
                         GpioMpsseController)


def main():
    argparser = ArgumentParser(description=modules[__name__].__doc__)
    argparser.add_argument('device',
                           help='serial port device name')
    args = argparser.parse_args()

    if not args.device:
        argparser.error('Serial device not specified')

    if args.device == 'search':
        read_one_byte('ftdi:///?', 0, 0)

    else:
        loop()

def loop():
    try:
        gpio = GpioAsyncController()
        gpio.configure('ftdi:///1', direction=0x60)
        while True:
            # all output set low
            # gpio.write(0x00)
            # all output set high
            # gpio.write(0x76)
            # all output set high, apply direction mask
            # gpio.write(0xFF & gpio.direction)
            # all output forced to high, writing to input pins is illegal
            # gpio.write(0xFF)  # raises an IOError
            user_input = prompt('ft232h gpio> ')
            if user_input == '':
                print('AD6(o) AD5(o) AD4(i) AD3(i): 0x%x'%((gpio.read() & 0x7f) >> 3))
            elif user_input in ['00', '01', '10', '11']:
                index = ['00', '01', '10', '11'].index(user_input)
                index = index << 5
                gpio.write(index & gpio.direction)
                print('AD6(o) AD5(o) AD4(i) AD3(i): 0x%x'%((gpio.read() & 0x7f) >> 3))
            else:
                print('not support command.')
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(traceback.format_exc())
    finally:
        gpio.close()
        print('Bye.')


if __name__ == '__main__':
    main()

