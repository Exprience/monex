from django.conf.urls import include, url, patterns, handler400, handler403, handler404, handler500
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app.user.forms import UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm
from django.contrib.auth import views

handler404 = 'app.web.views.handler404'
handler500 = 'app.web.views.handler500'

urlpatterns = [

	url(r'^', include('app.web.urls', namespace = 'web')),
    
    url(r'^user/', include('app.user.urls', namespace = 'user')),

    url(r'^manager/', include('app.manager.urls', namespace = 'manager')),

    url(r'^chat/', include('app.chat.urls', namespace = 'chat')),

    url(r'^competition/', include('app.competition.urls', namespace = 'competition')),

    url(r'^online_support/', include('app.online_support.urls', namespace = 'online_support')),

    url(r'^platform/', include('app.platform.urls', namespace = 'online_support')),

    url(r'^redactor/', include('redactor.urls')),
    
    url(r'^captcha/', include('captcha.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG is False:
	
    urlpatterns += patterns('',
		url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)
