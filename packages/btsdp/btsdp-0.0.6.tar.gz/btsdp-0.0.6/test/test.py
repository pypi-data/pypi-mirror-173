#!/usr/bin/env python

import os

from xpycommon.log import Logger, DEBUG

from btl2cap import PSMs

from btsdp import DataElement, DataElementTypes, UUID_L2CAP
from btsdp.fuzzer import SdpServerFuzzer


logger = Logger(__name__, DEBUG)


def main():
    
    # Fuzzer
    target_bd_addr = os.environ['BD_ADDR_HUAWEI_MATE_X2']
    logger.debug("target_bd_addr: {}".format(target_bd_addr))
    
    
    sdp_server_fuzzer = SdpServerFuzzer()
    sdp_server_fuzzer.connect(target_bd_addr)
    sdp_server_fuzzer.run()
    sdp_server_fuzzer.disconnect()


if __name__ == '__main__':
    main()
