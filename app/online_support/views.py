# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic as g
from app.web.get_username import *

class OnlineSupportView(g.TemplateView):
	template_name = 'online_support/online_support.html'

	def dispatch(self, request, *args, **kwargs):
		if not get_all_logged_in_users():
			return HttpResponse('Байхгүй байна')
		return super(OnlineSupportView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(OnlineSupportView, self).get_context_data(*args, **kwargs)
		print get_all_logged_in_users()
		return context