from django.conf.urls import url
from .views import *

urlpatterns = [

	url(r'^$', Home.as_view(), name = 'home'),
	url(r'^about/$', About.as_view(), name = 'about'),
	url(r'^news/$', News.as_view(), name = 'news'),
	url(r'^news/(?P<id>[0-9]+)/$', News.as_view(), name = 'news'),
	url(r'^news/view/(?P<id>[0-9]+)/$', NewsSelf.as_view(), name = 'news_self'),
	url(r'^research/(?P<id>[0-9]+)/$', Research.as_view(), name = 'research'),
	url(r'^lesson/(?P<id>[0-9]+)/$', Lesson.as_view(), name = 'lesson'),
	url(r'^contact/$', Contact.as_view(), name = 'contact'),
	url(r'^competition/$', WebCompetitionCalendar.as_view(), name = 'competition_calendar'),
	url(r'^contact/$', Contact.as_view(), name = 'contact'),
	url(r'^calendar/$', Calendar.as_view(), name = 'calendar'),
]