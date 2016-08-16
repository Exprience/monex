#!/usr/bin/env python
# -*- coding: utf-8 -*-


import session


class UserAuthMiddleware(object):

	def process_request(self, request):
		request.user = None
		try:
			user = session.get(request, 'user')
			request.user = user
		except:
			pass