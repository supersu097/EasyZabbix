#!/usr/bin/env python
# coding=utf-8
import argparse
from core import *

parser=argparse.ArgumentParser(
    description='Verify the config file whether it is right!'
)
parser.add_argument(
    '-c','--config',
    help='Config file location',
    type =file,
    required=True
)

zapi=common.getzapi(parser)

print 'Check success!'

