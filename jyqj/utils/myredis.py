# -*- coding: utf-8 -*-

from django.conf import settings
import redis
import os, sys


class MyRedis(redis.Redis):
    def __init__(self, **kwargs):
        host = settings.REDIS_HOST
        port = int(settings.REDIS_PORT)
        password = settings.REDIS_PASSWORD
        redis.Redis.__init__(self, host=host, port=port, password=password)

    def setvalue(self, key, value, time=None):
        self.set(key, value)
        if time:
            self.expire(key, time)

    def getvalue(self, key):
        value = self.get(key)
        if value:
                return value
        else:
            return None


MyRedisConnector = MyRedis()
