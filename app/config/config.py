# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import hashlib
import random
import string
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta


NULL_TEXT = u"Талбар хоосон байна"

URL_ERROR = u"URLERROR"
SYSTEM_ERROR = u"ERROR"

URL_ERROR_MESSAGE = u"Холболтонд алдаа гарлаа та засагдтал түр хүлээнэ үү."
SYSTEM_ERROR_MESSAGE = u"Системд алдаа гарлаа та засагдтал түр хүлээнэ үү."
UNIQUE_USERNAME = u'Хэрэглэгчийн нэр бүртгэлтэй байна'
UNIQUE_EMAIL = u'Хэрэглэгчийн и-мэйл бүртгэлтэй байна'


NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
PREVIOUS = (datetime.now() - relativedelta(month=1)).strftime("%Y-%m-%d %H:%M:%S")


def password():
    chars = string.ascii_uppercase + string.digits
    password = ''.join(random.sample(chars*6, 6))
    return password

def convert_2_10(create, update, delete):
    num1 = 0
    num2 = 0
    num3 = 0

    if create != 0:
        num1 = math.pow(2, 2)

    if update != 0:
        num2 = math.pow(2, 1)

    if delete != 0:
        num3 = math.pow(2, 0)

    return int(num1 + num2 + num3)


def convert_10_2(value):
    lists = []
    for i in str(format(int(value), '#05b')):
        lists.append(str(i))
    lists = lists[2:5]
    return lists

def get_dict(values):
    lists = []
    if hasattr(values, '__keylist__'):
        context = {}
        for key in values.__keylist__:
            #context[key] = getattr(values, key).value
            if hasattr(getattr(values, key), 'value'):
                context[key] = unicode(getattr(values, key).value)
            else:
                context[key] = u"Бичлэг байхгүй байна"
        lists.append(context)
    else:
        for value in values:
            context = {}
            for key in value.__keylist__:
                if hasattr(getattr(value, key), 'value'):
                    context[key] = unicode(getattr(value, key).value)
                else:
                    context[key] = u"Бичлэг байхгүй байна"
            lists.append(context)
    return lists



class Flash(object):

    def __init__(self, request):
        self.request = request

    def notice(self, message):
        self.request.session['_flash_notice'] = message

    def has_notice(self):
        return '_flash_notice' in self.request.session

    def get_notice(self):
        if self.has_notice():
            return self.request.session.pop('_flash_notice')
        return ''


    def warning(self, message):
        self.request.session['_flash_warning'] = message

    def has_warning(self):
        return '_flash_warning' in self.request.session

    def get_warning(self):
        if self.has_warning():
            return self.request.session.pop('_flash_warning')
        return ''


    def error(self, message):
        self.request.session['_flash_error'] = message

    def has_error(self):
        return '_flash_error' in self.request.session

    def get_error(self):
        if self.has_error():
            return self.request.session.pop('_flash_error')
        return ''