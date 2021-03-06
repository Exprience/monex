from django.conf.urls import url
from .views import *

urlpatterns = [

	url(r'^$', Home.as_view(), name = 'home'),
	url(r'^about/$', About.as_view(), name = 'about'),
	url(r'^news/$', News.as_view(), name = 'news'),
	url(r'^news/(?P<id>[0-9]+)/$', News.as_view(), name = 'news'),
	url(r'^news/view/(?P<id>[0-9]+)/$', NewsSelf.as_view(), name = 'news_self'),
	url(r'^research/$', Research.as_view(), name = 'research'),
	url(r'^research/filter/$', ResearchFilter.as_view(), name = 'research_filter'),
	#url(r'^research/(?P<id>[0-9]+)/$', Research.as_view(), name = 'research'),
	url(r'^lesson/$', Lesson.as_view(), name = 'lesson'),
	url(r'^lesson/filter/$', LessonFilter.as_view(), name = 'lesson_filter'),
	url(r'^lesson/mail/(?P<user_id>[0-9]+)/(?P<video_id>[0-9]+)/$', LessonMailView.as_view(), name = 'lesson_mail'),
	url(r'^contact/$', Contact.as_view(), name = 'contact'),
	url(r'^competition/$', WebCompetitionCalendar.as_view(), name = 'competition_calendar'),
	url(r'^competition/filter/$', WebCompetitionCalendarFilter.as_view(), name = 'competition_calendar_filter'),
	url(r'^contact/$', Contact.as_view(), name = 'contact'),
	url(r'^calendar/$', Calendar.as_view(), name = 'calendar'),
	url(r'^calendar/filter/$', CalendarFilter.as_view(), name = 'calendar_filter'),
	url(r'^bagts/$', BagtsView.as_view(), name = 'bagts'),
	url(r'^competition/register/(?P<id>[0-9]+)/$', WebCompetitionRegisterView.as_view(),
		name = 'web_competition_register'),
]