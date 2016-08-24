# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django.shortcuts import render_to_response
from django.template import RequestContext


def handler404(request):
	response = render_to_response('config/handler/404.html', {},
                                  context_instance=RequestContext(request))
	response.status_code = 404
	return response




def handler500(request):
    response = render_to_response('config/handler/505.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response