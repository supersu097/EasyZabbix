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

parser=common.Args(parser)
zapi=parser.getzapi()

print 'Check success!'

