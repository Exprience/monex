# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import re
import base64

from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views import generic as g
from django.forms.utils import ErrorList
from django.contrib.messages.views import SuccessMessageMixin
import managers as cm



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

	def get_template_names(self):
		if self.template_name is None:
			cname = self.__class__.__name__
			name = re.sub('(.)([A-Z][a-z]+)', r'\1%s\2' % '_', cname)
			name = re.sub('([a-z0-9])([A-Z])', r'\1%s\2' % '_', name).lower()
			namef = re.sub('(.)([A-Z][a-z]+)', r'\1%s\2' % '/', cname)
			namef = re.sub('([a-z0-9])([A-Z])', r'\1%s\2' % '/', namef).lower()
			# get app_label
			app_path = self.__module__[:-len('.views')][len('app.'):]
			app_path = app_path.replace('.', '/')
			# prepare template name
			self.template_names = ['%s/ui/%s.html' % (app_path, name), '%s/%s.html' % (app_path, name), '%s/ui/%s.html' % (app_path, namef), '%s/%s.html' % (app_path, namef)]
			return self.template_names
		return super(BaseMixin, self).get_template_names()

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


class File(g.View):

    def get(self, request, *args, **kwargs):
    	file = self.kwargs.get('file', None)
        if file:
            f = cm.BaseDataManager.get_file("1", file)
            #content_type = 'application/pdf'
            content_type = 'image/png'
            return HttpResponse(base64.b64decode(f.file), content_type=content_type)
        else:
            raise Http404
        return super(File, self).get(request, *args, **kwargs)