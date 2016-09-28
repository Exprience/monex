# !/usr/bin/python/env
# -*- coding:utf-8 -*-

from django.conf.urls import url
import views as v

app_name = 'platform'


urlpatterns = [
	url(r'^(?P<pk>[0-9]+)/$', v.HomeView.as_view(), name = 'home'),
	url(r'^news/(?P<pk>[0-9]+)/$', v.NewsView.as_view(), name = 'news'),
	url(r'^account/$', v.AccountView.as_view(), name = 'account'),
	url(r'^def/$', v.Default.as_view(), name = 'default'),
	url(r'^stock/(?P<pk>[0-9]+)/$', v.StockView.as_view(), name = 'stock'),
	url(r'^currency/(?P<pk>[0-9]+)/$', v.CurrencyView.as_view(), name = 'currency'),
	url(r'^currency/buy/(?P<cid>[0-9]+)/(?P<vid>[0-9]+)/$', v.CurrencyBuyView.as_view(), name = 'currency_buy'),
	url(r'^alert/$', v.AlertView.as_view(), name = 'alert'),
	#url(r'^order/', OrderView.as_view(), name='order'),
	#url(r'^calendar/', CalendarView.as_view(), name='calendar'),
	
]