from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', CompetitionHome.as_view(), name = 'competition_home'),
]