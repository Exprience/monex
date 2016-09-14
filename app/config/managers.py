# !/usr/bin/env/python
# -*- coding:utf-8 -*-


import logging
import suds


from django.conf import settings
from django.core.cache import cache


from suds.plugin import DocumentPlugin, MessagePlugin
from suds.client import Client
from suds.bindings import binding


__all__ = ['BaseDataManager']


class LogPlugin(MessagePlugin):
    def sending(self, context):
        print('sending', str(context.envelope))
    def received(self, context):
        print('received', str(context.reply))


class FixUrls(DocumentPlugin):
    def loaded(self, ctx):
        ctx.document = ctx.document.replace('a-PC', settings.WS_SERVER).replace('192.168.1.20', settings.WS_SERVER).replace('localhost:9080', '%s:9080' % settings.WS_SERVER).replace('STATIC_URL', settings.STATIC_DOMAIN_URL)
        return ctx


class BaseDataManager(object):
    __instance = None

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if BaseDataManager.__instance is None:
            BaseDataManager.__instance = BaseDataManager()
        return BaseDataManager.__instance



    def setup_client(self, wsdl_url, serverAddressFilled=False):
        logging.basicConfig(level=logging.ERROR)
        headers = {'Content-Type': 'application/soap+xml; charset="UTF-8"'}
        url = '%s%s' % ('http://%s:9080' % settings.WS_SERVER if not serverAddressFilled else '', wsdl_url)
        if settings.DEBUG:
            client = Client(url, timeout=90, cachingpolicy=1, plugins = [FixUrls(), LogPlugin()])
        else:
            client = Client(url, timeout=90, cachingpolicy=1, plugins = [FixUrls()])
        client.options.cache.clear()
        return client
