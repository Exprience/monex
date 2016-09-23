# !/usr/bin/python/env
# -*- coding:utf-8 -*-

from django.conf.urls import url
from views import HomeView, NewsView, AccountView , Default#,  OrderView, CalendarView, PopView

app_name = 'platform'


urlpatterns = [
	url(r'^$', HomeView.as_view(), name = 'home'),
	url(r'^news/$', NewsView.as_view(), name = 'news'),
	url(r'^account/$', AccountView.as_view(), name = 'account'),
	url(r'^def/$', Default.as_view(), name = 'default'),
	#url(r'^order/', OrderView.as_view(), name='order'),
	#url(r'^calendar/', CalendarView.as_view(), name='calendar'),
	
]