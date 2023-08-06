#!/usr/bin/env python

import sys
import logging

from xpycommon.log import Logger, DEBUG

sys.path.insert(0, '/home/x/OneDrive/Projects/btl2cap/src')
from btl2cap import CID_BR_EDR_SECURITY_MANAGER

sys.path.insert(0, '/home/x/OneDrive/Projects/btsm/src')
from btsm import SecurityMaanger


logger = Logger(__name__, logging.DEBUG)


NEXUS_5_BD_ADDR = '58:3F:54:47:9A:1D'
HUAWEI_MATE_X2_BD_ADDR = 'A0:DE:0F:89:68:93'


def test_smp_over_le():
    pass


def test_smp_over_acl_u():
    pass


def main():
    test_smp_over_acl_u()


if __name__ == '__main__':
    main()
