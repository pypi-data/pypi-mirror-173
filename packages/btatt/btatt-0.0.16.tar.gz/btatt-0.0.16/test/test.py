#!/usr/bin/env python

import sys
import struct

sys.path.insert(0, "/home/x/OneDrive/Projects/btatt/src")
from btatt import ATT_READ_BY_GROUP_TYPE_REQ
from btatt import AttClient

print(sys.argv)

def __test():
    print("btatt test")
    att_client = AttClient()

                    # address       address type, 0 public, 1 random
    att_client.connect(sys.argv[1], sys.argv[2])
    # handles = [0x0102, 0x0104]
    # data = att_client.read_multiple_variable_req(handles)
    # data = att_client.read_multiple_req(handles)
    # print(data)
    
    # 使能 Service changed 的 indication
    # data = att_client.write_req(0x0003, b'\x20\x00')
    # print(data)
    
    # data = att_client.exchange_mtu_req(24)
    # print(data)
    # rsp = att_client.write_req(0x0018, b'\x41\x41')
    # print(rsp)
    
    # mal_uuid = b'\x00\x01\x02'*5
    # pdu = struct.pack('<BHH{}s'.format(len(mal_uuid)), ATT_READ_BY_GROUP_TYPE_REQ.opcode, 0x0001, 0xffff, mal_uuid)
    # data = att_client.send(pdu)
    # print(data)
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    
    att_client.disconnect()

if __name__ == '__main__':
    __test()
