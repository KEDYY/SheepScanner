#!/usr/bin/env python2
#-*- coding: utf-8 -*-
u"""
1. 调用nmap 全网 80 端口开放式扫描，汇总开放的 IP 返回的探测信息（OS HTTPSERVER）
2. 调用分布式抓取，worker 分工 将1 中的可用的ip 等分派给worker 纳入探测
3. 获取对应的返回信息（是否是http服务器，服务器返回信息包括跳转等）反查询域名等
4. 其他相关的信息
一般来讲 task 是将一个大任务拆分为小任务了，每个task都是小任务，这里先管功能
"""
from __future__ import absolute_import
from celery import shared_task

import logging
logger = logging.getLogger(__name__)

import uuid
import json
class Worker(object):
    u"""
    抽象类，用于实现各种Worker
    """
    def __init__(self, name, discribe, path):
        super(object)
        self.name = name
        self.id = uuid.uuid1()
        self.discribe = discribe
        self.path = path.split('/')

    def about_me(self):
        me = {'id': str(self.id),
              'location': self.path,
              'name': self.name,
              'discribe': self.discribe
        }
        return json.dumps(me)

import requests
class HttpHeaderFetcher(Worker):
    count = 0 
    u"""
    用于获取服务器HTTP头信息
    """
    def __init__(self, http_address, http_port):
        Worker.__init__(self, 'HttpHeaderFetcher', 'fetch http header of server response', '/tcp/Woker/fetcher-%d' %  HttpHeaderFetcher.count)
        self.address = http_address
        self.port    = http_port
        HttpHeaderFetcher.count += 1

    def run(self):
        server = "http://{0}:{1}/".format(self.address, self.port)
        headers = {'User-Agent': "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}        
        response = None
        try:
            response = requests.get(server, headers=headers, timeout=3, allow_redirects=False)
        except Exception as (e):
            error = "GET {0} Error: {1}".format(server, e.message)
            logger.error(error)
            return dict(ok=False, server="", error=error)
        else:
            if response:
                if response.status_code == 200:
                    return dict(ok=True, server=response.headers['server'])
                else:
                    return dict(ok=True, server=response.headers['server'])
            else:
                logger.warn("status:%s" % response.status_code)
                return dict(ok=False, server='')
import socket as scks
class SocksFetcher(Worker):
    count = 0
    def __init__(self, address, port):
        Worker.__init__(self, 'Socks v5 Fetcher', 'check the address is socks proxy server', '/tcp/Worker/fetcher-%d' % SocksFetcher.count)
        self.address = address
        self.port    = port
        SocksFetcher.count += 1
    
    def run(self):
        pck = '\x05\x01\x00'
        rsp = '\x05\x00'
        fd = scks.socket(scks.AF_INET, scks.SOCK_STREAM)
        try:
            fd.connect((self.address, self.port))
            fd.send(pck)
            ret = fd.recv(1024)
            fd.close()
            if ret.startswith(rsp):
                return dict(ok=True)
        except Exception:
            return dict(ok=False)

@shared_task
def http(host_name):
    f1 = HttpHeaderFetcher(host_name, 80)
    res = f1.run()
    if res['ok']:
         res.update(dict(host=host_name))
    else:
        logger.warn("host failed![%s]" % host_name)
        res.update(dict(host=host_name))
    return res

import nmap
import os
from dao.DB import HostScannerDB
@shared_task
def scan_host(host, ports='1-65535'):
    u"""
    最小化任务，仅扫描一个ip
    """
    sudo = False
    scan_args = '-sT -Pn'
    if os.getuid() == 0:
        sudo = True
        scan_args = '-sS -Pn'
    def call_back(host, scan_data):
        logger.debug("Scan Host {0} complate: {1}".format(host, scan_data))
        
    scanner = nmap.PortScannerAsync()
    logger.debug("Add task Scan Host `{0}` with Ports {1}".format(host, ports))

    scanner.scan(str(host), str(ports), scan_args, callback=call_back, sudo=sudo)
    return dict(ok=True)
        
@shared_task
def socksv5(hosts, ports):
    if type(hosts) in (str, unicode):
        if type(ports) in (str, unicode, int):
            sf = SocksFetcher(hosts, ports)
            return sf.run()
        else:
            res = dict()
            for port in ports:
                sf = SocksFetcher(hosts, port)
                res.update({"{0}{1}".format(hosts, port): sf.run()})   
            return res
    else:
        res = dict()
        for host in hosts:
            if type(ports) in (str, unicode, int):
                sf = SocksFetcher(host, ports)
                res.update({"{0}{1}".format(host, ports): sf.run()})
            else:
                res = dict()
                for port in ports:
                    sf = SocksFetcher(host, port)
                    res.update({"{0}{1}".format(host, port): sf.run()})
        return res


def test():
    http('123.34.2.1')
    socksv5('192.168.233.1', '1080')

if __name__ == '__main__':
    test()
