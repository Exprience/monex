#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import url
import views as v


app_name="web"


urlpatterns = [


	url(r'^$', v.Home.as_view(), name = 'home'),

	
	url(r'^news/$', v.News.as_view(), name = 'news'),
	url(r'^news/(?P<id>[0-9]+)/$', v.News.as_view(), name = 'news'),
	url(r'^news/view/(?P<pk>[0-9]+)/$', v.NewsSelf.as_view(), name = 'news_view'),
	

	url(r'^research/$', v.Research.as_view(), name = 'research'),
	url(r'^research/filter/$', v.ResearchFilter.as_view(), name = 'research_filter'),

	
	url(r'^lesson/$', v.Lesson.as_view(), name = 'lesson'),
	url(r'^lesson/filter/$', v.LessonFilter.as_view(), name = 'lesson_filter'),
	url(r'^lesson/mail/(?P<user_id>[0-9]+)/(?P<video_id>[0-9]+)/$', v.LessonMailView.as_view(), name = 'lesson_mail'),
	

	url(r'^competition/$', v.Competition.as_view(), name = 'competition'),
	url(r'^competition/filter/$', v.WebCompetitionCalendarFilter.as_view(), name = 'competition_calendar_filter'),
	url(r'^competition/register/(?P<pk>[0-9]+)/$', v.CompetitionRegisterView.as_view(), name = 'competition_register'),


	url(r'^calendar/$', v.Calendar.as_view(), name = 'calendar'),
	url(r'^calendar/filter/$', v.CalendarFilter.as_view(), name = 'calendar_filter'),
	url(r'^bagts/$', v.BagtsView.as_view(), name = 'bagts'),

	
]