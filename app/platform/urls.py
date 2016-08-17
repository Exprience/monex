# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django.conf.urls import url
from views import Home


app_name = 'competition'


urlpatterns = [
	url(r'^$', Home.as_view(), name = 'home'),
]