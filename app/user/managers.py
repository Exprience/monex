import logging
import suds
import hashlib
from datetime import datetime
from django.conf import settings

from django.core.cache import cache

from suds.plugin import DocumentPlugin, MessagePlugin
from suds.client import Client
from suds.bindings import binding



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



    @staticmethod
    def check_unique_user(status, value):
        try:
            client = BaseDataManager.get_instance().setup_client('/MX_Check_Duplicate_Username_Email_HTTPService/MX_Check_Duplicate_Username_Email_HTTPPort?wsdl')
            result = client.service.MX_Check_Duplicate_Username_Email_HTTPOperation(status, value)
            return result
        except:
            return None



    @staticmethod
    def loginUser(username, password):
        try:
            client = BaseDataManager.get_instance().setup_client('/MX_Check_User_LoginService/MX_Check_User_LoginPort?wsdl')
            result = client.service.MX_Check_User_LoginOperation(username, hashlib.md5(password).hexdigest(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            user = User()
            user.fill_user(result)
            return user
        except:
            return None

    @staticmethod
    def register(username, email, password):
        try:
            client = BaseDataManager.get_instance().setup_client('/MX_User_RegistrationService/MX_User_RegistrationPort?wsdl')
            result = client.service.MX_User_RegistrationOperation(username, '', '', hashlib.md5(password).hexdigest(), False, email, False, False, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return result
        except:
            return None


class User(object):

    def is_authenticated(self):
        return True

    def fill_user(self, data):
        self.id = data.id
        self.isHavePrivilege = data.isHavePrivilege
        self.last_login = data.last_login
        self.is_superuser = data.is_superuser
        self.is_staff = data.is_staff
        self.is_active = data.is_active
        self.firstname =  data.firstname
