#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import Celery

app = Celery('SheepScanner',  include=['sheepscan.tasks'])

if __name__ == '__main__':
    app.start()
