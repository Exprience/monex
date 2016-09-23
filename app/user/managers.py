# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import hashlib
from urllib2 import URLError
from datetime import datetime


from app.config.managers import BaseDataManager
from app.config import config

class UserBaseDataManager(BaseDataManager):

    @staticmethod
    def check_unique_user(status, value):
        try:
            client = UserBaseDataManager.get_instance().setup_client('/MX_Check_Duplicate_Username_Email_HTTPService/MX_Check_Duplicate_Username_Email_HTTPPort?wsdl')
            result = client.service.MX_Check_Duplicate_Username_Email_HTTPOperation(status, value, False)
            return result
        except URLError:
            return config.URL_ERROR
        except Exception, e:
            return config.SYSTEM_ERROR

    @staticmethod
    def login(username, password):
        try:
            client = UserBaseDataManager.get_instance().setup_client('/MX_Check_User_LoginService/MX_Check_User_LoginPort?wsdl')
            result = client.service.MX_Check_User_LoginOperation(username, hashlib.md5(password).hexdigest(), config.NOW)
            print result
            user = User()
            user.fill_user(result)
            return user
        except:
            return config.SYSTEM_ERROR

    @staticmethod
    def register(username, email, password):
        try:
            client = UserBaseDataManager.get_instance().setup_client('/MX_User_RegistrationService/MX_User_RegistrationPort?wsdl')
            result = client.service.MX_User_RegistrationOperation(username, '', '', hashlib.md5(password).hexdigest(), False, email, False, False, config.NOW)
            return result
        except:
            return config.SYSTEM_ERROR


class User(object):
    
    def is_authenticated(self):
        return True

    def fill_user(self, data):
        for key in data.__keylist__:
            if hasattr(getattr(data, key), 'value'):
                if key == "last_login":
                    self.last_login = datetime.strptime(data.last_login, "%Y-%m-%d %H:%M:%S")
                else:
                    print key
                    setattr(self, key, getattr(data, key).value)
            else:
                if key == "last_login":
                    self.last_login = datetime.strptime(data.last_login, "%Y-%m-%d %H:%M:%S")
                else:
                    setattr(self, key, getattr(data, key))

    def is_user(self):
        return True
