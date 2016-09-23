# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views import generic as g
from django.forms.utils import ErrorList

def handler404(request):
	response = render_to_response('config/handler/404.html', {},
                                  context_instance=RequestContext(request))
	response.status_code = 404
	return response




def handler500(request):
    response = render_to_response('config/handler/500.html', {},
                                  context_instance=RequestContext(request))
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
		self.form_class._errors["__all__"] = ErrorList([message])


class FormView(BaseMixin, g.FormView):
	pass


class TemplateView(BaseMixin, g.TemplateView):
	pass