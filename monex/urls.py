from django.conf.urls import include, url, patterns, handler400, handler403, handler404, handler500
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app.user.forms import UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm
from django.contrib.auth import views

#handler400 = 'my_app.views.bad_request'
#handler403 = 'my_app.views.permission_denied'
handler404 = 'app.web.views.handler404'
handler500 = 'app.web.views.handler500'

urlpatterns = [

	url(r'^', include('app.web.urls', namespace = 'web')),
    
    url(r'^user/', include('app.user.urls', namespace = 'user')),

    url(r'^manager/', include('app.manager.urls', namespace = 'manager')),

    url(r'^chat/', include('app.chat.urls', namespace = 'chat')),

    url(r'^competition/', include('app.competition.urls', namespace = 'competition')),

    url(r'^online_support/', include('app.online_support.urls', namespace = 'online_support')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^redactor/', include('redactor.urls')),
    
    url(r'^captcha/', include('captcha.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url('^inbox/notifications/', include('notifications.urls', namespace='notifications')),


    url(r'^password_reset/$', views.password_reset, {
        'template_name' : 'user/password/password_reset.html',
        'password_reset_form' : UserPasswordResetForm,
        'post_reset_redirect' : 'web:home',
        }, name='password_reset'),
    
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', views.password_reset_confirm, {
        'template_name' : 'user/password/password_reset_confirm.html',
        'set_password_form': UserSetPasswordForm,
        'post_reset_redirect' : 'web:home'
        }, name ='password_reset_confirm'),
    
    url(r'^reset_done/$', views.password_reset_complete,
        {'template_name' : 'user/password/password_reset_complete.html' }, name ='password_reset_complete'),

    url(r'^change_password/$', views.password_change, {
        'template_name' : 'user/password/password_change.html',
        'password_change_form' : UserPasswordChangeForm,
        'post_change_redirect' : 'web:home',
        }, name="password_change"),

    #url(r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', views.password_reset_confirm, {
    #    'template_name' : 'user/password/password_reset_confirm.html',
    #    'set_password_form': UserSetPasswordForm,
    #    'post_reset_redirect' : 'web:home',
    #    },
    #    name ='password_confirm'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG is False:
	
    urlpatterns += patterns('',
		url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)
