# !/usr/bin/env/python
# -*- coding:utf-8 -*-

import os
import logging
import suds
import base64


from django.conf import settings
from django.core.cache import cache


from suds.plugin import DocumentPlugin, MessagePlugin
from suds.client import Client
from suds.bindings import binding


# Export
__all__ = ['BaseDataManager']


# Log бичих
class LogPlugin(MessagePlugin):
    def sending(self, context):
        pass
        #print('sending', str(context.envelope))
    def received(self, context):
        pass
        #print('received', str(context.reply))


class FixUrls(DocumentPlugin):
    def loaded(self, ctx):
        ctx.document = ctx.document.replace('a-PC', settings.WS_SERVER).replace('192.168.1.3', settings.WS_SERVER).replace('localhost:9080', '%s:9080' % settings.WS_SERVER).replace('STATIC_URL', settings.STATIC_DOMAIN_URL)
        return ctx


class BaseDataManager(object):
    __instance = None

    """Singleton patterns хэрэгжүүлсэн класс"""

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

    @staticmethod
    def get_file(manager_id, file):
        client = BaseDataManager.get_instance().setup_client('/MXGetFileByPatternWSDLService/MXGetFileByPatternWSDLPort?wsdl')
        result = client.service.MXGetFileByPatternWSDLOperation(manager_id, file)
        print "##################################"
        print "##################################"
        print "##################################"
        print "##################################"
        print "##################################"
        print dir(result)
        print "##################################"
        print "##################################"
        print "##################################"
        print "##################################"
        print "##################################"
        return result
    
    @staticmethod
    def file_upload(type, id, file_name, file_url):
        client = BaseDataManager.get_instance().setup_client("/MX_Manager_File_UploadService/MX_Manager_File_UploadPort?wsdl")
        with open(str(file_url), "rb") as f:
            data = f.read()
            file = base64.b64encode(data)
            file_type = os.path.splitext(file_url)[1][1:]
            name = os.path.splitext(file_name)[0]
        result = client.service.MX_Manager_File_UploadOperation(type, id, name, file_type, file)
        return result