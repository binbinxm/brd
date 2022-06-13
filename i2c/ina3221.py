#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
read/write ina3221
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
    argparser.add_argument('offset', type=str,
                           help='internal register offset of the device')
    argparser.add_argument('data', type=str, nargs='?', default=None,
                           help='write value, hex format, if this value is empty then I assume it\'s a read operation')
    args = argparser.parse_args()

    if not args.device:
        argparser.error('Serial device not specified')

    if args.device == 'search':
        read_one_byte('ftdi:///?', 0, 0)

    elif args.data == None:
        args.addr = int(args.addr, base=16)
        args.offset = int(args.offset, base=16)

        value = read_one_byte(args.device, args.addr, args.offset)
        print('register address = 0x%02x,  read value = 0x%02x'%(args.offset, value))

    else:
        args.addr = int(args.addr, base=16)
        args.offset = int(args.offset, base=16)
        args.data = int(args.data, base=16)

        write_one_byte(args.device, args.addr, args.offset, args.data)
        print('register address = 0x%02x, write value = 0x%02x'%(args.offset, args.data))

def read_one_byte(url, addr, offset):
    i2c = I2cController()
    value = False
    try:
        i2c.configure(url)
        slave = i2c.get_port(addr)
        slave.write(offset.to_bytes(1,'big'), start=True, relax=True)
        sleep(0.001)
        tmp = slave.read(2, start=True, relax=True)
        value = int.from_bytes(tmp, 'big')
    except Exception as e:
        print(traceback.format_exc())
    finally:
        i2c.close()
        return value

def write_one_byte(url, addr, offset, data):
    i2c = I2cController()
    try:
        i2c.configure(url)
        slave = i2c.get_port(addr)
        slave.write(offset.to_bytes(1,'big'), start=True, relax=False)
        sleep(0.001)
        string = data.to_bytes(2,'big')
        print(string)
        slave.write(string, start=False, relax=True)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        i2c.close()

if __name__ == '__main__':
    main()

