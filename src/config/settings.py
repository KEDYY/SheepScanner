# -*- coding: utf-8 -*-
mongo = {
    'name': 'mongodb',
    'host': '192.168.233.1',
    'port': 27017,
    'db'  : 'SheepScanner',
    'collection.task' : 'sheepscan_taskmeta',
    'collection.result.webscan' : 'web_status',
    'collection.result.hostscan' : 'host_status'
}

web = {
    'host': '0.0.0.0',
    'port': 8080,
    'debug': True
}

u"""
若使用Redis 作为Broker 则 需要安装 redis 模块
$[sudo] pip install redis
"""
#redis = {
#    'name': 'redis',
#    'host': '127.0.0.1',
#    'port': 6379,
#    'db'  : 'SheepScanner'
#}
