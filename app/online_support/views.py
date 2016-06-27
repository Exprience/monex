# -*- coding:utf-8 -*-
import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic as g
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from app.web.get_username import *
from .forms import SupportUserMessageForm
from app.manager.models import *
from .models import SupportMessage, Support
from app.user.models import SystemUser


class OnlineSupportView(g.FormView):
	template_name = 'online_support/online_support.html'
	form_class = SupportUserMessageForm
	success_url = reverse_lazy('online_support')

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		manager = Manager.objects.get(username = 'manager')
		system_user = SystemUser.objects.get(id = request.user.id)
		if not Support.objects.filter(manager = manager, system_user = system_user):
			self.message = Support.objects.create(manager = manager, system_user = system_user)
		else:
			self.message = Support.objects.get(manager = manager, system_user = system_user)
		#if not get_all_logged_in_users():
		#	return HttpResponse('Байхгүй байна')
		return super(OnlineSupportView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(OnlineSupportView, self).get_context_data(*args, **kwargs)
		context['managers'] = True #get_all_logged_in_users()
		context['messages'] = SupportMessage.objects.filter(
			support = self.message,
			support_date__startswith = datetime.now().date())
		return context

	def form_valid(self, form):
		model = form.save(commit = False)
		model.support = self.message
		model.save()
		res = {
			'id':model.id,
			'msg':model.system_user_message,
			'user':model.support.system_user.username,
			'time':model.support_date.strftime('%I:%M:%S %p').lstrip('0')
			}
		data = json.dumps(res)
		return HttpResponse(data,content_type="application/json")
		#return super(OnlineSupportView, self).form_valid(form)

def support_message_view(request):
	messages = SupportMessage.objects.filter(support__system_user = request.user.id)
	c = []
	for m in messages:
		c.append({
			'manager': m.support.manager.username ,
			'user': m.support.system_user.username,
			'manager_msg': m.manager_message,
			'user_msg': m.system_user_message,
			'time': m.support_date.strftime('%I:%M:%S %p').lstrip('0')
		})
	data = json.dumps(c)
	return HttpResponse(data, content_type="application/json")