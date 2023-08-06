#!/usr/bin/env python

import sys
sys.path.insert(0, '/home/x/OneDrive/Projects/btl2cap/src')

from ctypes import sizeof
from xpycommon import libc


from socket import SOCK_SEQPACKET
from btl2cap import L2capSock, p_sockaddr_l2, sockaddr_l2
from btl2cap import CIDs

from btl2cap.fuzz import L2capFuzzer

def main():
    # sock = L2capSock(bdaddr='11:22:33:44:55:66')
    # l2addr = sockaddr_l2()
    # libc.getsockname(sock.fileno(), p_sockaddr_l2(l2addr), sizeof(l2addr))
    # print(sock.getsockname())
    
    # print(l2addr.l2_family)
    # print(l2addr.l2_psm)
    # print(l2addr.l2_bdaddr)
    # print(l2addr.l2_cid)
    # print(l2addr.l2_bdaddr_type)

    # fuzzer = L2capFuzzer('hci0')
    # print(fuzzer)
    
    print(1 in (None, CIDs))

if __name__ == '__main__':
    main()
