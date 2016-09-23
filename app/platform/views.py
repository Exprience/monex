# !/usr/bin/python/env
 #, widget = forms.Select()
# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.views import generic as g
from django.views.generic import TemplateView, FormView
from forms import PriceAlertForm, OrderForm, AccountForm


class HomeView(FormView):
	template_name = 'competition/trade.html'
	form_class = PriceAlertForm

class OrderView(FormView):
	form_class = OrderForm
	template_name = 'competition/trade/stock.html'

class CalendarView(TemplateView):
	template_name = 'competition/news/calendar.html'

class NewsView(TemplateView):
	template_name = 'competition/news.html'
class AccountView(TemplateView):
	template_name = 'competition/account.html'
class Default(TemplateView):
	template_name = 'competition/default.html'
class AccountInfoView(object):
		template_name = 'competition/account/untitled.html'
		form_class= AccountForm
			