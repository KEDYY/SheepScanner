#!/usr/bin/env python2
#-*- coding: utf-8 -*-
u"""
CELERY 配置
"""
from .settings import mongo
try:
    from .settings import redis as broker
except ImportError:
    from .settings import mongo as broker
#BROKER_BACKEND = "mongodb"
#BROKER_URL = 'mongodb://192.168.233.1:27017/demo_zz'
BROKER_URL = '{0}://{1}:{2}/{3}'.format(broker['name'], broker['host'], broker['port'], broker['db'] )

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER='json'
CELERY_RESULT_BACKEND = mongo['name']
CELERY_MONGODB_BACKEND_SETTINGS = {
    'host': mongo['host'],
    'port': mongo['port'],
    'database': mongo['db'],
    'taskmeta_collection': mongo['collection.task']
}
