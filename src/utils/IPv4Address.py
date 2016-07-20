#!/usr/bin/env python
# -*- coding: utf-8 -*-
# support python2 python3
__all__=['belong2us', 'is_ipv4', 'genarateIPv4', 'genarateIPv4CIDR']
import traceback
def ipv4(addr):
    """IPv4: a.b.c.d"""
    a, b, c, d = addr.split('.')
    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)
    assert a in range(256)
    assert b in range(256)
    assert c in range(256)
    assert d in range(256)
    return a, b, c, d

import sys
from binascii import hexlify
def belong2us(addr, network, mask):
    """All your base are belong to us"""
    assert isIPaddr(addr), "input address is not ipv4 address"
    assert isIPaddr(network), "network format error"
    assert mask in range(33), "mask format error"
    ma = ipv4(addr)
    mb = ipv4(network)
    binaryaddr = b''
    for x,y in zip(ma, mb):
        # PYTHON2
        if sys.version[0]=='2':
            binaryaddr += chr(x^y)
        # PYTHON 2&3
        elif sys.version[0]=='3':
            binaryaddr += bytearray(chr(x^y), "ISO-8859-1")
    b01 = bin(int(hexlify(binaryaddr), 16)).replace('0b0', '').replace('0b', '')
    return (32-len(b01) >= mask)

def is_ipv4(addr, skip_local=False):
    if not isIPaddr(addr):
       return False
    if skip_local:
        if belong2us(addr, "10.0.0.0", 8) or \
                belong2us(addr, "127.0.0.0", 8) or \
                belong2us(addr, "172.16.0.0", 11) or \
                belong2us(addr, "192.168.0.0", 16):
            return False
    return True

def isIPaddr(addr):
    """ a.b.c.d  0-255 """
    try:
        a, b, c, d =  ipv4(addr)
    except Exception:
        return False
    else:
        return True
    
def genarateIPv4(start, end):
    """
    36.96.0.0	36.223.255.255
    """
    try:
        ma = ipv4(start)
        mb = ipv4(end)

        int32_start = ma[0]*pow(2, 24) + ma[1]*pow(2, 16) + ma[2]*pow(2, 8) + ma[3]
        int32_end   = mb[0]*pow(2, 24) + mb[1]*pow(2, 16) + mb[2]*pow(2, 8) + mb[3]
        for i in range(int32_start, int32_end+1):
            yield toIPv4Str(i)
    except Exception:
        traceback.print_exc()

def genarateIPv4CIDR(reg):
    u"""
    20.4657759666s  2555904
    55.0284800529s  6750208
    134.817610979s 16777216
    """
    try:
        network, mask = reg.split('/')
        mask = int(mask)
        a, b, c, d = ipv4(network)
        assert mask in range(33), "ipv4 netmask must be in range(33)"
        int32_mask = int(mask * '1' + (32-mask) * '0', 2)
        int32_addr = a*pow(2, 24) + b*pow(2, 16) + c*pow(2, 8) + d

        start_addr = int32_addr & int32_mask
        assert start_addr <= int32_addr, "be sure network with argument {0} eq {1}!".format(network, toIPv4Str(start_addr))
        hosts_numb = pow(2, 32-mask)
        for i in range(int32_addr, start_addr+hosts_numb):
            yield toIPv4Str(i)
        
    except Exception:
        traceback.print_exc()

def toIPv4Str(int32):
    hexstr = hex(int32).replace('0x', '').replace('L', '')
    if len(hexstr) % 2 != 0:
        hexstr = '0' + hexstr
    assert len(hexstr) == 8, "argument {0} is not 32bits int number".format(hexstr)
    a = int(hexstr[:2], 16)
    b = int(hexstr[2:4], 16)
    c = int(hexstr[4:6], 16)
    d = int(hexstr[6:8], 16)
    return "{0}.{1}.{2}.{3}".format(a, b, c, d)

def test():
    assert belong2us('192.168.1.1', '192.168.1.0', 32) is False
    from time import time
    t1 = time()
    for i in range(1000000):
        assert belong2us('192.168.1.1', '192.168.1.1', 32) is True
    print (time()-t1)
    # python2 code only 7.12s
    # python3 code only 5.6s
    # python2 & 3 code :python2 9.19s, python3 6.26s
    for ip in genarateIPv4('192.168.0.1', '192.168.0.255'):
        print(ip)

    for ip in genarateIPv4CIDR('34.0.0.0/24'):
        print(ip)

def main(argv):
    if len(argv) != 4:
        print("Usage:  $python %s IP NETWORK MASK\nSuch AS $python %s 192.168.1.187 192.168.1.187 32" %(argv[0], argv[0]))
        sys.exit(-1)
    ip = argv[1]
    net = argv[2]
    mask = int(argv[3])
    if belong2us(ip, net, mask):
        print("IP belongs the NETWORK")
    else:
        print("IP:[%s] not in Network:[%s]" % (ip, net))
import sys
if __name__ == '__main__':
    main(sys.argv)
    #test()

