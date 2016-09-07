# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django.conf.urls import url
import views as v


app_name = 'user'


urlpatterns = [
	url(r'^$', v.UserHome.as_view(), name = 'home'),
	url(r'^login/$', v.UserLogin.as_view(), name = 'login'),
    url(r'^register/$', v.UserRegisterView.as_view(), name = 'register'),
    url(r'^logout/$', v.UserLogin.logout, name = 'logout'),
    url(r'^password_reset/$', v.UserResetPasswordView.as_view(), name= 'password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', v.UserSetPassView.as_view(), name= 'password_reset_confirm'),
    url(r'^change_password/$', v.UserChangePasswordView.as_view(), name="password_change"),
]