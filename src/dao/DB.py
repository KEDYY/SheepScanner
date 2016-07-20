__author__ = 'neon'

import pymongo
from config.settings import mongo

class MongoDB(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._connect_()

    def _connect_(self):
        self.client = pymongo.MongoClient(*self.args, **self.kwargs)

    def __del__(self):
        self.client.close()

class WebScannerDB(MongoDB):

    def __init__(self, host, port, *args, **kwargs):
        MongoDB.__init__(self, host, port, *args, **kwargs)
        self.db = self.client[mongo['db']]
        self.coll = self.db[mongo['collection.result.webscan']]

    def query_result(self, task_uuid):
        return self.coll.find({'_id': task_uuid})

    def find(self):
        return self.coll.find()

class HostScannerDB(MongoDB):

    def __init__(self, host, port, *args, **kwargs):
        MongoDB.__init__(self, host, port, *args, **kwargs)
        self.db = self.client[mongo['db']]
        self.coll = self.db[mondo['collection.result.hostscan']]

    def query_result(self, task_uuid):
        return self.coll.find({'_id': task_uuid})

    def find(self):
        return self.coll.find()


if __name__ == '__main__':
    wdb = WebScannerDB('127.0.0.1', 27017)
    hdb = HostScannerDB('127.0.0.1', 27017)
