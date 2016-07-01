from django.conf.urls import url
import views as v

app_name = 'user'

urlpatterns = [
	url(r'^$', v.Home.as_view(), name = 'home'),
	url(r'^login/$', v.Login.as_view(), name = 'login'),
    url(r'^register/$', v.RegisterView.as_view(), name = 'register'),
    url(r'^logout/$', v.Login.logout, name = 'logout'),
]