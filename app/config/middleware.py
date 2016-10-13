# !/usr/bin/python/env
# -*- coding: utf-8 -*-

import session
from app.config.config import Flash

class AuthMiddleware(object):

	def process_request(self, request):
		request.user = None
		try:
			user = session.get(request, 'user')
			manager = session.get(request, 'manager')
			if user:
				request.user = user
			else:
				request.user = manager
		except:
			pass

class FlashMiddleware(object):

	def process_request(self, request):
		request.flash = Flash(request)

	def process_template_response(self, request, response):
		response.context_data.update({
			'flash': Flash(request),
		})
		return response