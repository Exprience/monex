# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django.conf.urls import include, url, patterns, handler400, handler403, handler404, handler500
from django.conf import settings
from django.conf.urls.static import static


handler404 = 'app.config.views.handler404'
handler500 = 'app.config.views.handler500'


urlpatterns = [

	url(r'^', include('app.web.urls', namespace = 'web')),
    
    url(r'^user/', include('app.user.urls', namespace = 'user')),

    url(r'^manager/', include('app.manager.urls', namespace = 'manager')),

    url(r'^chat/', include('app.chat.urls', namespace = 'chat')),

    url(r'^competition/', include('app.competition.urls', namespace = 'competition')),

    url(r'^online_support/', include('app.online_support.urls', namespace = 'online_support')),

    url(r'^redactor/', include('redactor.urls')),
    
    url(r'^captcha/', include('captcha.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG is False:
	
    urlpatterns += patterns('',
		url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)
