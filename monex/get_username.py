# -*- coding:utf-8 -*-
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import HttpResponse

from django.utils.translation import ugettext as _
_requests = {}

def get_username():
	t = 'request_user'
	if t not in _requests:
		return None
	return _requests[t]

class RequestMiddleware(object):

	#def __init__(self):
	#	pass

	def process_request(self, request):
		_requests['request_user'] = request

	#def process_view(self, *args, **kwargs):
	#	print "Fasdfasdf"

	#def process_exception(self):
	#	print "fasdfasdfasfdasdfasdfasdfaf"		

	#def process_template_response(self, *args, **kwargs):
	#	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~`"

	#def process_response(self, *args, **kwargs):
	#	return HttpResponse("Uuganaa")




def get_all_logged_in_users():
	sessions = Session.objects.filter(expire_date__gte=timezone.now())
	uid_list = []

	for session in sessions:
		data = session.get_decoded()
		uid_list.append(data.pop('_auth_user_id', None))

	return Manager.objects.filter(id__in = uid_list, groups__name = _(u'Оператор'))