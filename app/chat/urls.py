# -*- coding:utf-8 -*-

from django.conf.urls import url
from .views import *

app_name = 'chat'

urlpatterns = [
	url(r'^$', RoomView.as_view(), name = 'room'),
	url(r'^(?P<id>[0-9]+)/$', ChatView.as_view(), name = 'chat'),
	url(r'^message/(?P<id>[0-9]+)/$', message, name = 'message'),
]