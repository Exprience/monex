# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import hashlib
from datetime import datetime


from app.config.managers import BaseDataManager


class UserBaseDataManager(BaseDataManager):


    @staticmethod
    def check_unique_user(status, value):
        try:
            client = UserBaseDataManager.get_instance().setup_client('/MX_Check_Duplicate_Username_Email_HTTPService/MX_Check_Duplicate_Username_Email_HTTPPort?wsdl')
            result = client.service.MX_Check_Duplicate_Username_Email_HTTPOperation(status, value, False)
            return result
        except:
            return None

    @staticmethod
    def loginUser(username, password):
        try:
            client = UserBaseDataManager.get_instance().setup_client('/MX_Check_User_LoginService/MX_Check_User_LoginPort?wsdl')
            result = client.service.MX_Check_User_LoginOperation(username, hashlib.md5(password).hexdigest(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            user = User()
            user.fill_user(result)
            return user
        except:
            return None

    @staticmethod
    def register(username, email, password):
        try:
            client = UserBaseDataManager.get_instance().setup_client('/MX_User_RegistrationService/MX_User_RegistrationPort?wsdl')
            result = client.service.MX_User_RegistrationOperation(username, '', '', hashlib.md5(password).hexdigest(), False, email, False, False, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return result
        except:
            return None


class User(object):
    
    isHavePrivilege = False

    def is_authenticated(self):
        return True

    def fill_user(self, data):
        self.id = None
        self.isHavePrivilege = data.isHavePrivilege
        self.last_login = data.last_login
        self.is_superuser = data.is_superuser.value
        self.is_staff = data.is_staff.value
        self.is_active = data.is_active.value
        if hasattr(data.firstname, 'value'):
            self.firstname =  data.firstname.value
        else:
            self.firstname = None
