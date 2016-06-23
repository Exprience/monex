from django.conf.urls import url
from .views import *

urlpatterns = [

	url(r'^$', OnlineSupportView.as_view(), name = 'online_support'),
]