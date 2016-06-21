from django.conf.urls import url
from .views import Login, RegisterView, login

urlpatterns = [
	url(r'^login/$', Login.as_view(), name = 'login'),
    url(r'^register/$', RegisterView.as_view(), name = 'register'),
    url(r'^logout/$', Login.logout, name = 'logout'),
]