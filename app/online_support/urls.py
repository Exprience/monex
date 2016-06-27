from django.conf.urls import url
from .views import *

urlpatterns = [

	url(r'^$', OnlineSupportView.as_view(), name = 'online_support'),
	url(r'^support/$', support_message_view, name = 'support_message'),
]