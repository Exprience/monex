# !/usr/bin/python/env
# -*- coding:utf-8 -*-

from django.conf.urls import url
import views as v

app_name = 'platform'


urlpatterns = [
	url(r'^(?P<pk>[0-9]+)/$', v.Platform.as_view(), name = 'home'),
	url(r'^news/(?P<pk>[0-9]+)/$', v.News.as_view(), name = 'news'),
	#url(r'^account/$', v.AccountView.as_view(), name = 'account'),
		
	url(r'^currency/(?P<pk>[0-9]+)/$', v.Currency.as_view(), name = 'currency'),
	url(r'^currency/package/(?P<pk>[0-9]+)/$', v.CurrencyPackage.as_view(), name = 'currency_package'),
	url(r'^currency/buy/(?P<cid>[0-9]+)/(?P<vid>[0-9]+)/$', v.CurrencyBuy.as_view(), name = 'currency_buy'),
	url(r'^currency/sell/(?P<cid>[0-9]+)/(?P<pid>[0-9]+)/$', v.CurrencySell.as_view(), name = 'currency_sell'),

	#url(r'^stock/(?P<pk>[0-9]+)/$', v.Stock.as_view(), name = 'stock'),
	#url(r'^stock/value/(?P<pk>[0-9]+)/$', v.StockValueView.as_view(), name = 'stock_value'),
	#url(r'^stock/buy/(?P<cid>[0-9]+)/(?P<sid>[0-9]+)/$', v.StockBuyView.as_view(), name = 'stock_buy'),
	#url(r'^stock/sell/(?P<cid>[0-9]+)/(?P<sid>[0-9]+)/$', v.StockSellView.as_view(), name = 'stock_sell'),

	url(r'^alert/(?P<pk>[0-9]+)/$', v.Alert.as_view(), name = 'alert'),
	url(r'^alert/create/(?P<pk>[0-9]+)/$', v.AlertCreate.as_view(), name = 'alert_create'),
	url(r'^alert/update/(?P<pk>[0-9]+)/(?P<id>[0-9]+)/$', v.AlertUpdate.as_view(), name = 'alert_update'),
	url(r'^alert/delete/(?P<pk>[0-9]+)/(?P<id>[0-9]+)/$', v.AlertDelete.as_view(), name = 'alert_delete'),
	#url(r'^order/', OrderView.as_view(), name='order'),
	#url(r'^calendar/', CalendarView.as_view(), name='calendar'),
	
]