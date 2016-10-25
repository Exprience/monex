# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django import http


import forms as f
from app.config import status, config, views as cv
from app.web.managers import WebDataManager as wm
from app.manager.managers import ManagerDataManager as mm
from managers import PlatformDataManager as pm
from app.manager import models


class FormView(cv.FormView):

	def get_context_data(self, *args,  **kwargs):
		context = super(FormView, self).get_context_data(*args, **kwargs)
		context['pk'] = self.pk
		return context

class TemplateView(cv.TemplateView):

	def get_context_data(self, *args,  **kwargs):
		context = super(TemplateView, self).get_context_data(*args, **kwargs)
		context['pk'] = self.pk
		return context


class Platform(TemplateView):

	def get(self, request, *args, **kwargs):
		competition = mm.individually("", "C", self.pk)
		if not wm.if_register(self.pk, request.user.id) or str(competition.status.value) == status.COMPETITION_START_REGISTER:
			raise http.Http404
		return super(Platform, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(Platform, self).get_context_data(*args, **kwargs)
		currencys = mm.list("L", config.PREVIOUS, config.NOW)
		for currency in currencys:
			if currency['currency_id'] == u"1":
				currency['name'] = "USDMNT"
				value = models.Currency.objects.filter(name = "USDMNT").order_by('id').reverse()
				if currency['buy'] > value[1].buy:
					currency['buy_change'] = '1'
				elif currency['buy'] < value[1].buy:
					currency['buy_change'] = '0'

				if currency['sell'] > value[1].sell:
					currency['sell_change'] = '1'
				elif currency['sell'] < value[1].sell:
					currency['sell_change'] = '0'

			if currency['currency_id'] == u"2":
				currency['name'] = "USDEUR"
				value = models.Currency.objects.filter(name = "USDEUR").order_by('id').reverse()
				if currency['buy'] > value[1].buy:
					currency['buy_change'] = '1'
				elif currency['buy'] < value[1].buy:
					currency['buy_change'] = '0'

				if currency['sell'] > value[1].sell:
					currency['sell_change'] = '1'
				elif currency['sell'] < value[1].sell:
					currency['sell_change'] = '0'
			if currency['currency_id'] == u"3":
				currency['name'] = "USDKRW"
				value = models.Currency.objects.filter(name = "USDKRW").order_by('id').reverse()
				if currency['buy'] > value[1].buy:
					currency['buy_change'] = '1'
				elif currency['buy'] < value[1].buy:
					currency['buy_change'] = '0'

				if currency['sell'] > value[1].sell:
					currency['sell_change'] = '1'
				elif currency['sell'] < value[1].sell:
					currency['sell_change'] = '0'
			if currency['currency_id'] == u"4":
				currency['name'] = "USDJPY"
				value = models.Currency.objects.filter(name = "USDJPY").order_by('id').reverse()
				if currency['buy'] > value[1].buy:
					currency['buy_change'] = '1'
				elif currency['buy'] < value[1].buy:
					currency['buy_change'] = '0'

				if currency['sell'] > value[1].sell:
					currency['sell_change'] = '1'
				elif currency['sell'] < value[1].sell:
					currency['sell_change'] = '0'
			if currency['currency_id'] == u"5":
				currency['name'] = "USDRUB"
				value = models.Currency.objects.filter(name = "USDRUB").order_by('id').reverse()
				if currency['buy'] > value[1].buy:
					currency['buy_change'] = '1'
				elif currency['buy'] < value[1].buy:
					currency['buy_change'] = '0'

				if currency['sell'] > value[1].sell:
					currency['sell_change'] = '1'
				elif currency['sell'] < value[1].sell:
					currency['sell_change'] = '0'

		context['currencys'] = currencys
		packages = pm.currency("S", self.pk, self.request.user.id)
		for package in packages:
			
			currency = mm.list("I", config.PREVIOUS, config.NOW, id = package['buy_currency_value_id'])[0]
			
			package['sell'] = currency['sell']
			if currency['currency_id'] == u"1":
				package['name'] = "USDMNT"
				package['buy_now'] = models.Currency.objects.filter(name = 'USDMNT').last().buy
			elif currency['currency_id'] == u"2":
				package['name'] = "USDEUR"
				package['buy_now'] = models.Currency.objects.filter(name = 'USDEUR').last().buy
			elif currency['currency_id'] == u"3":
				package['name'] = "USDKRW"
				package['buy_now'] = models.Currency.objects.filter(name = 'USDKRW').last().buy
			elif currency['currency_id'] == u"4":
				package['name'] = "USDJPY"
				package['buy_now'] = models.Currency.objects.filter(name = 'USDJPY').last().buy
			elif currency['currency_id'] == u"5":
				package['name'] = "USDRUB"
				package['buy_now'] = models.Currency.objects.filter(name = 'USDRUB').last().buy
		
		context['packages'] = packages
		return context


class Stock(TemplateView):

	def get_context_data(self, *args, **kwargs):
		context = super(Stock, self).get_context_data(*args, **kwargs)
		context['stocks'] = mm.list("L", config.PREVIOUS, config.NOW, is_currency = False)
		return context

class StockValueView(TemplateView):
	template_name = "platform/trade/position_stock.html"

	def get_context_data(self, *args, **kwargs):
		context = super(StockValueView, self).get_context_data(*args, **kwargs)
		context['packages'] = pm.currency("S", self.pk, self.request.user.id, isCurrency = False)
		return context

class StockBuyView(FormView):

	form_class = f.StockBuyForm
	template_name = "platform/stock/buy.html"
	success_url = "/"

	def dispatch(self, request,*args,**kwargs):
		self.cid = int(self.kwargs.pop("cid", None))
		self.sid = int(self.kwargs.pop("sid", None))
		return super(StockBuyView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(StockBuyView, self).get_context_data(*args, **kwargs)
		context['stock'] = mm.list("I", config.PREVIOUS, config.NOW, id = self.sid, is_currency = False)[0]
		return context

	def form_valid(self, form):
		piece = form.cleaned_data['piece']
		pm.currency("C", self.cid, self.request.user.id, piece = piece, value_id = self.sid, isCurrency = False)
		return super(StockBuyView, self).form_valid(form)

class StockSellView(FormView):
	form_class = f.StockBuyForm
	template_name = "platform/stock/sell.html"
	success_url = "/"

	def dispatch(self, request,*args,**kwargs):
		self.cid = int(self.kwargs.pop("cid", None))
		self.sid = int(self.kwargs.pop("sid", None))
		return super(StockSellView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(StockSellView, self).get_context_data(*args, **kwargs)
		return context

	def form_valid(self, form):
		pm.currency("U", self.cid, self.request.user.id, value_id = 3, id = self.sid, isCurrency = False)
		return super(StockSellView, self).form_valid(form)


class Currency(Platform):
	pass

class CurrencyPackage(Platform):
	pass

class CurrencyBuy(FormView):
	form_class = f.CurrencyBuyForm
	success_url = "/"

	def dispatch(self, request,*args,**kwargs):
		self.cid = int(self.kwargs.pop("cid", None))
		self.vid = int(self.kwargs.pop("vid", None))
		return super(CurrencyBuy, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(CurrencyBuy, self).get_context_data(*args, **kwargs)
		currency = mm.list("I", config.PREVIOUS, config.NOW, id = self.vid)[0]
		if currency['currency_id'] == u"1":
			currency['name'] = "USDMNT"
		elif currency['currency_id'] == u"2":
			currency['name'] = "USDEUR"
		elif currency['currency_id'] == u"3":
			currency['name'] = "USDKRW"
		elif currency['currency_id'] == u"4":
			currency['name'] = "USDJPY"
		elif currency['currency_id'] == u"5":
			currency['name'] = "USDRUB"
		context['currency'] = currency
		return context

	def form_valid(self, form):
		piece = form.cleaned_data['piece']
		pm.currency("C", self.cid, self.request.user.id, piece = piece, value_id = self.vid)
		return super(CurrencyBuy, self).form_valid(form)

class CurrencySell(FormView):
	form_class = f.CurrencyBuyForm
	success_url = "/"

	def dispatch(self, request,*args,**kwargs):
		self.cid = int(self.kwargs.pop("cid", None))
		self.pid = int(self.kwargs.pop("pid", None))
		return super(CurrencySell, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(CurrencySell, self).get_context_data(*args, **kwargs)
		return context

	def form_valid(self, form):
		pm.currency("U", self.cid, self.request.user.id, value_id = 3, id = self.pid)
		return super(CurrencySell, self).form_valid(form)


class NewsView(TemplateView):
	
	template_name = 'platform/news.html'

	def get_context_data(self, *args, **kwargs):
		context = super(NewsView, self).get_context_data(*args, **kwargs)
		context['news'] = mm.select(u"", u'N')
		return context


class AlertView(TemplateView):
	
	template_name = "platform/trade/alert.html"


class OrderView(FormView):
	form_class = f.OrderForm
	template_name = 'platform/trade/stock.html'


class CalendarView(TemplateView):
	
	template_name = 'platform/news/calendar.html'


class AccountView(TemplateView):
	
	template_name = 'platform/account.html'


class Default(TemplateView):
	
	template_name = 'platform/default.html'


class AccountInfoView(object):
	template_name = 'platform/account/untitled.html'
	form_class= f.AccountForm
			