#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
write ltc2635
"""

#pylint: disable-msg=broad-except
#pylint: disable-msg=too-few-public-methods

from time import sleep
import traceback

from argparse import ArgumentParser, FileType
from logging import Formatter, StreamHandler, getLogger, DEBUG, ERROR
from sys import modules, stderr
from traceback import format_exc
from pyftdi import FtdiLogger
from pyftdi.ftdi import Ftdi
from pyftdi.i2c import I2cController, I2cNackError
from pyftdi.misc import add_custom_devices


def main():
    argparser = ArgumentParser(description=modules[__name__].__doc__)
    argparser.add_argument('device',
                           help='serial port device name')
    argparser.add_argument('addr', type=str,
                           help='i2c bus address, hex format 0x50 for example')
    argparser.add_argument('cmd', type=str,
                           help='cmd << 4 + addr, hex format')
    argparser.add_argument('data', type=str,
                           help='write value, 16 bits, hex format')
    args = argparser.parse_args()

    if not args.device:
        argparser.error('Serial device not specified')

    if args.device == 'search':
        read_one_byte('ftdi:///?', 0, 0)

    else:
        args.addr = int(args.addr, base=16)
        args.cmd = int(args.cmd, base=16)
        args.data = int(args.data, base=16)

        write_one_byte(args.device, args.addr, args.cmd, args.data)
        print('register address = 0x%02x, write value = 0x%02x'%(args.cmd, args.data))

def write_one_byte(url, addr, cmd, data):
    i2c = I2cController()
    try:
        i2c.configure(url)
        slave = i2c.get_port(addr)
        string = cmd.to_bytes(1,'big') + data.to_bytes(2,'big')
        slave.write(string, start=True, relax=True)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        i2c.close()

if __name__ == '__main__':
    main()

