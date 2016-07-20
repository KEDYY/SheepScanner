#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import Response

from flask import logging
from celery import Celery

import json
import sys
import os
sys.path.append(''.join([os.getcwd() ]))
app = Flask(__name__)

logger = logging.getLogger(__name__)


from dao.DB import WebScannerDB
from utils.IPv4Address import is_ipv4
celery_app = Celery('SheepScanner', include=['sheepscan.tasks'])
celery_app.config_from_object('config.celery')

db = WebScannerDB('192.168.233.1', 27017)

@app.route('/')
def main():
    index = u"""
    <html>
        <head>
            <meta http-equiv="content-type" content="text/html;charset=utf-8">
            <title>管理平台</title>
        </head>
        <body>
        <p>REST API 返回JSON结果</p>
        <ul>
            <li>/tasks/all 显示所有任务ID</li>
            <li>/tasks/add?ip=ip_address 添加IP地址任务</li>
            <li>/tasks/status?task_id=task_id 查看任务状态</li>
        </ul>
        </body>
    </html>
    """
    return index#Response(index.encode("utf-8"), status=200, content_type='application/json' )

@app.route('/scan/add')
def add_scan():
    iprange = request.args['hosts']
    portrange = request.args.get('ports', 80, type=int)
    result = celery_app.send_task("sheepscan.tasks.scan_host", args=[iprange, portrange]) or None
    if result:
        return json.dumps(dict(status=0, task_id=result.id))
    else:
        return json.dumps(dict(status=1))

@app.route('/tasks/add')
def add_task():
    ip_address = request.args['ip']
    if not is_ipv4(ip_address, skip_local=True):
        return Response("""{status=1, info="invalid ip address!"}""", status=200, content_type='application/json' )
    # 增加任务
    #celery_app.test.task(ip_address)
    result = celery_app.send_task("sheepscan.tasks.http", args=[ip_address]) or None
    if result:
        return json.dumps(dict(status=0, task_id=result.id))
    else:
        return json.dumps(dict(status=1))

@app.route('/socks/add')
def add_socks():
    ip_address = request.args['ip']
    port = request.args.get('port', 1080, type=int)
    if not is_ipv4(ip_address, skip_local=True):
        return Response("""{status=1, info="invalid ip address!"}""", status=200, content_type='application/json' )
    result = celery_app.send_task("sheepscan.tasks.socksv5", args=[ip_address, port]) or None
    if result:
        return json.dumps(dict(status=0, task_id=result.id))
    else:
        return json.dumps(dict(status=1))

@app.route('/tasks/status')
def show_result():
    task_uuid = request.args['task_id']
    res = db.query_result(task_uuid)
    count = res.count()
    if count < 1:
        return Response("""{status=1, info="no founded!"}""", status=200, content_type='application/json' )
    elif count == 1:
        rep = dict(status=0)
        rep.update(**res[0])
        rep['date_done'] = rep.get('date_done').isoformat(' ')
        return Response(json.dumps(rep), status=200, content_type='application/json' )
    else:
        return Response("""{status=1, info="no founded!"}""", status=200, content_type='application/json' )

@app.route('/tasks/all')
def show_all_task():
    res = db.find()
    uids = []
    for r in res:
        uids.append(r['_id'])
    rep = dict(status=0, tasks=uids)
    return Response(json.dumps(rep), status=200, content_type='application/json' )

if __name__ == '__main__':
    from config.settings import web
    app.run(web['host'], web['port'], debug=web['debug'], threaded=True)
