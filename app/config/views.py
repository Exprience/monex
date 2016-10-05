# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views import generic as g
from django.forms.utils import ErrorList
from django.contrib.messages.views import SuccessMessageMixin

def handler404(request):
	if hasattr(request.user, "is_manager"):
		template_name = "config/handler/manager404.html"
	else:
		template_name = 'config/handler/404.html'
	response = render_to_response(template_name, {},
                                  context_instance=RequestContext(request))
	response.status_code = 404
	return response




def handler500(request):
	if hasattr(request.user, "is_manager"):
		template_name = "config/handler/manager500.html"
	else:
		template_name = 'config/handler/500.html'
	response = render_to_response(template_name, {}, context_instance=RequestContext(request))
	response.status_code = 500
	return response


class BaseMixin(object):

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(BaseMixin, self).dispatch(request, *args, **kwargs)

	def notice(self, message):
		self.request.flash.notice(message)

	def warning(self, message):
		self.request.flash.warning(message)

	def error(self, message):
		self.request.flash.error(message)

	def form_error(self, form, message):
		form._errors["__all__"] = ErrorList([message])
		return self.form_invalid(form)


class FormView(SuccessMessageMixin, BaseMixin, g.FormView):
	success_message = u"Мэдээлэл амжилттай хадгалагдлаа"


class TemplateView(BaseMixin, g.TemplateView):
	pass