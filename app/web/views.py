#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re


from django.views import generic as g
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


import forms as f
from app.manager import models as mmodels
from app.config import config, views as v
from app.user import views as user_v
from app.manager.managers import ManagerDataManager as mm
from managers import WebDataManager as wm

#Exports
__all__ = []

class BaseMixin(object):

	def get_context_data(self, *args, **kwargs):
		context = super(BaseMixin, self).get_context_data(*args, **kwargs)
		context['breaking_news'] = mm.select("", 'N', value1 = "1")
		context['usdeur'] = mmodels.Currency.objects.filter(name = "USDEUR").last()
		context['usdmnt'] = mmodels.Currency.objects.filter(name = "USDMNT").last()
		context['usdjpy'] = mmodels.Currency.objects.filter(name = "USDJPY").last()
		context['usdkrw'] = mmodels.Currency.objects.filter(name = "USDKRW").last()
		context['usdrub'] = mmodels.Currency.objects.filter(name = "USDRUB").last()
		return context


class NotManager(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user and hasattr(request.user, 'is_manager'):
			return HttpResponseRedirect(reverse_lazy('manager:home'))
		return super(NotManager, self).dispatch(request, *args, **kwargs)


class Home(NotManager, v.TemplateView):

	def get_context_data(self, *args, **kwargs):
		context = super(Home, self).get_context_data(*args, **kwargs)
		
		news = mm.select("", 'N')
		news = news[0]
		path = re.compile(r'<img [^>]*src="([^"]+)')
		url = path.findall(news['body'])
		if url:
			news['img_url'] = url[0]
		context['news'] = news

		lesson = mm.select("", "L")[0]
		lesson['image'] = "http://img.youtube.com/vi/%s/0.jpg"%lesson['url'][32:]
		context['lesson'] = lesson
		return context


class News(BaseMixin, NotManager, v.TemplateView):

	template_name = 'web/news/news.html'

	def get_context_data(self, *args, **kwargs):
		context = super(News, self).get_context_data(*args, **kwargs)
		news = mm.select("", 'N')
		for n in news:			
			path = re.compile(r'<img [^>]*src="([^"]+)')
			url = path.findall(n['body'])
			if url:
				n['img_url'] = url[0]
		paginator = Paginator(news, 5)
		page = self.request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
			contacts = paginator.page(1)
		except EmptyPage:
			contacts = paginator.page(paginator.num_pages)
		context['newss'] = contacts
		return context

class NewsFilter(News):

	pass

class NewsDetail(BaseMixin, NotManager, v.TemplateView):
	template_name = 'web/news/news_self.html'

	def get_context_data(self, *args, **kwargs):
		context = super(NewsDetail, self).get_context_data(*args, **kwargs)
		context['news'] = mm.individually("", 'N', self.pk)
		return context


class Research(BaseMixin, NotManager, user_v.LoginRequired, v.TemplateView):
	
	template_name = 'web/research/research.html'

class ResearchFilter(Research):
	
	template_name = 'web/research/research_filter.html'


class Lesson(BaseMixin, NotManager, g.FormView):
	template_name = 'web/lesson/lesson.html'
	form_class = f.LessonMailForm

	def get_context_data(self, *args, **kwargs):
		context = super(Lesson, self).get_context_data(*args, **kwargs)
		lessons = mm.select("", 'L')
		for lesson in lessons:
			lesson['image'] = "http://img.youtube.com/vi/%s/0.jpg"%lesson['url'][32:]
		context['lessons'] = lessons
		return context

class LessonFilter(Lesson):
	
	template_name = 'web/lesson/lesson_filter.html'


class Competition(BaseMixin, NotManager, v.TemplateView):
	template_name = 'web/competition/competition.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Competition, self).get_context_data(*args, **kwargs)
		competitions = mm.select("", 'C')
		if competitions == config.URL_ERROR:
			pass
		else:
			context['competitions'] = competitions
		return context

class WebCompetitionCalendarFilter(Competition):
	
	template_name = 'web/competition/competition_filter.html'


class Calendar(BaseMixin, NotManager, v.TemplateView):
	
	template_name = 'web/calendar/calendar.html'

class CalendarFilter(Calendar):
	
	template_name = 'web/calendarWWW/calendar_filter.html'


class BagtsView(BaseMixin, NotManager, g.FormView):
	def __init__(self, *args, **kwargs):
		super(BagtsView, self).__init__(*args, **kwargs)
		self.title = "Тэмцээний ангилал"
		self.form_class = BagtsForm
		self.submit_button = ModalButton(value=u'Хадгалах', loading_value = "Уншиж байна...",
			button_type='success btn-flat')
		self.close_button = ModalButton(value=u'Хаах', button_type ='default btn-flat')

	def form_valid(self, form, **kwargs):
		self.response = ModalResponse('Амжилттай хадгалагдлаа', 'success')
		form.save()
		self.save(form)
		self.response = ModalResponse("{obj} is created".format(obj=self.object), 'success')
		return super(BagtsView, self).form_valid(form, commit = False, **kwargs)


class CompetitionRegisterView(BaseMixin, NotManager, user_v.LoginRequired, v.FormView):
	template_name = "web/competition/competition_register.html"
	form_class = f.CompetitionRegisterForm
	success_url = reverse_lazy('web:competition')

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionRegisterView, self).get_context_data(*args, **kwargs)
		return context

	def form_valid(self, form):
		obj = form.save()
		result = wm.register("C", file = obj.reciept, competition_id = self.pk, user_id = self.request.user.id)
		if result == config.SYSTEM_ERROR:
			self.error(config.SYSTEM_ERROR_MESSAGE)
			return self.form_invalid(form)
		return super(CompetitionRegisterView, self).form_valid(form)


class LessonMailView(BaseMixin, NotManager, v.FormView):

	def __init__(self, *args, **kwargs):
		super(LessonMailView, self).__init__(*args, **kwargs)
		self.title = u"Санал хүсэлт"
		self.form_class = f.LessonMailForm
		self.submit_button = ModalButton(value=u'Илгээх', loading_value = "Уншиж байна...",
			button_type='primary btn-flat')
		self.close_button = ModalButton(value=u'Хаах', button_type ='default btn-flat')

	def form_valid(self, form, **kwargs):
		self.response = ModalResponse('Таны мэйл амжилттай илгээгдлээ', 'success')
		subject = 'no reply'
		message = form.cleaned_data['feedback']
		user= form.cleaned_data['username']
		video = form.cleaned_data['video_name']
		#user = SystemUser.objects.get(id = self.kwargs.pop('user_id', None))
		#video = Surgalt.objects.get(id = self.kwargs.pop('video_id', None))
		message += user.email
		try:
			email = EmailMessage(subject, message, to = [video.author_email])
			email.send()
		except BadHeaderError:
			return HttpResponse('Амжилтгүй')
		return super(LessonMailView, self).form_valid(form, **kwargs)
