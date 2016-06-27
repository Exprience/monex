# -*- coding:utf-8 -*-
from django.contrib.sessions.models import Session
from django.utils import timezone


from app.manager.models import Manager
from django.utils.translation import ugettext as _
_requests = {}

def get_username():
	t = 'request_user'
	if t not in _requests:
		return None
	return _requests[t]

class RequestMiddleware(object):
	def process_request(self, request):
		_requests['request_user'] = request


def get_all_logged_in_users():
	sessions = Session.objects.filter(expire_date__gte=timezone.now())
	uid_list = []

	for session in sessions:
		data = session.get_decoded()
		uid_list.append(data.pop('_auth_user_id', None))

	return Manager.objects.filter(id__in = uid_list, groups__name = _(u'Оператор'))