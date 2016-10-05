# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django import http


import forms as f
from app.config import status, config, views as cv
from app.web.managers import WebDataManager as wm
from app.manager.managers import ManagerDataManager as mm
from managers import PlatformDataManager as pm


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


class HomeView(FormView):
	template_name = 'platform/trade.html'
	form_class = f.PriceAlertForm

	def get(self, request, *args, **kwargs):
		competition = mm.individually("", "C", self.pk)
		if not wm.if_register(self.pk, request.user.id) or str(competition.status.value) == status.COMPETITION_START_REGISTER:
			raise http.Http404
		return super(HomeView, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(HomeView, self).get_context_data(*args, **kwargs)
		context['currencys'] = mm.list("L", config.PREVIOUS, config.NOW)
		context['packages'] = pm.currency("S", self.pk, self.request.user.id)
		return context


class StockView(TemplateView):
	template_name = "platform/trade/stock.html"

	def get_context_data(self, *args, **kwargs):
		context = super(StockView, self).get_context_data(*args, **kwargs)
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


class CurrencyView(TemplateView):
	
	template_name = "platform/trade/currency.html"

	def get_context_data(self, *args, **kwargs):
		context = super(CurrencyView, self).get_context_data(*args, **kwargs)
		context['currencys'] = mm.list("L", config.PREVIOUS, config.NOW)
		return context

class CurrencyValueView(TemplateView):
	
	template_name = "platform/trade/position_currency.html"

	def get_context_data(self, *args, **kwargs):
		context = super(CurrencyValueView, self).get_context_data(*args, **kwargs)
		context['packages'] = pm.currency("S", self.pk, self.request.user.id)
		return context

class CurrencyBuyView(FormView):
	form_class = f.CurrencyBuyForm
	template_name = "platform/currency/buy.html"
	success_url = "/"

	def dispatch(self, request,*args,**kwargs):
		self.cid = int(self.kwargs.pop("cid", None))
		self.vid = int(self.kwargs.pop("vid", None))
		return super(CurrencyBuyView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(CurrencyBuyView, self).get_context_data(*args, **kwargs)
		context['currency'] = mm.list("I", config.PREVIOUS, config.NOW, id = self.vid)[0]
		return context

	def form_valid(self, form):
		piece = form.cleaned_data['piece']
		pm.currency("C", self.cid, self.request.user.id, piece = piece, value_id = self.vid)
		return super(CurrencyBuyView, self).form_valid(form)

class CurrencySellView(FormView):
	form_class = f.CurrencyBuyForm
	template_name = "platform/currency/sell.html"
	success_url = "/"

	def dispatch(self, request,*args,**kwargs):
		self.cid = int(self.kwargs.pop("cid", None))
		self.pid = int(self.kwargs.pop("pid", None))
		return super(CurrencySellView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(CurrencySellView, self).get_context_data(*args, **kwargs)
		return context

	def form_valid(self, form):
		pm.currency("U", self.cid, self.request.user.id, value_id = 3, id = self.pid)
		return super(CurrencySellView, self).form_valid(form)


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
			