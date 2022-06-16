#!/usr/bin/python3
# -*- coding: utf-8 -*-

# from argparse import ArgumentParser, FileType
# from sys import modules, stderr
# from time import sleep
# from pyftdi import FtdiLogger
# from pyftdi.ftdi import Ftdi
from pyftdi.i2c import I2cController, I2cNackError
# from pyftdi.misc import add_custom_devices
# import numpy as np
# import time

i2c = I2cController()
i2c.configure('ftdi:///')
slave = i2c.get_port(0x30)

#test demo 设置RST_PERST_MCU_L的引脚为高电平
slave.write(b'\x21\x01\x01')
slave.write(b'\x22\x01\x01')

#test demo 读取ALERT_SWBUS_LV18_L的引脚电平
slave.write(b'\x23\x02\x01\x01')
ack = slave.read(2)
print(ack)

print('end')
