# !/usr/bin/python/env
# -*- coding: utf-8 -*-


from app.config import session


class ManagerAuthMiddleware(object):

	def process_request(self, request):
		request.user = None
		try:
			user = session.get(request, 'manager')
			request.user = user
		except:
			pass