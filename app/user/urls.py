# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django.conf.urls import url
import views as v


app_name = 'user'


urlpatterns = [
	url(r'^$', v.Home.as_view(), name = 'home'),
	url(r'^login/$', v.Login.as_view(), name = 'login'),
    url(r'^register/$', v.RegisterView.as_view(), name = 'register'),
    url(r'^logout/$', v.Login.logout, name = 'logout'),
    url(r'^password_reset/$', v.ResetPasswordView.as_view(), name= 'password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', v.SetPasswordView.as_view(), name= 'password_reset_confirm'),
    url(r'^change_password/$', v.ChangePasswordView.as_view(), name="password_change"),
]