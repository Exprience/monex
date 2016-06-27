from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^(?P<token>.+)/$', CompetitionHome.as_view(), name = 'competition_home'),
]