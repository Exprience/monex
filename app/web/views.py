#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views import generic as g
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response


import forms as f
from app.config import config, views as v
from app.user import views as user_v
from app.manager.managers import ManagerBaseDataManager as mm
from managers import WebBaseDataManager as m

#Exports
__all__ = []

class NotManager(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user and hasattr(request.user, 'is_manager'):
			return HttpResponseRedirect(reverse_lazy('manager:manager_home'))
		return super(NotManager, self).dispatch(request, *args, **kwargs)



class Home(NotManager, v.TemplateView):
	template_name = 'web/home/home.html'


class News(NotManager, v.TemplateView):

	template_name = 'web/news/news.html'

	def get_context_data(self, *args, **kwargs):
		context = super(News, self).get_context_data(*args, **kwargs)
		context['newss'] = mm.select("", 'N')
		return context




class NewsSelf(NotManager, v.TemplateView):
	template_name = 'web/news/news_self.html'

	def get_context_data(self, *args, **kwargs):
		context = super(NewsSelf, self).get_context_data(*args, **kwargs)
		context['news'] = mm.individually("", 'N', self.kwargs['pk'])
		return context


class Research(NotManager, user_v.LoginRequired, v.TemplateView):
	template_name = 'web/research/research.html'




class ResearchFilter(Research):
	template_name = 'web/research/research_filter.html'




class Lesson(NotManager, g.FormView):
	template_name = 'web/lesson/lesson.html'
	form_class = f.LessonMailForm

	def get_context_data(self, *args, **kwargs):
		context = super(Lesson, self).get_context_data(*args, **kwargs)
		context['lessons'] = mm.select("", 'L')
		return context




class LessonFilter(Lesson):
	template_name = 'web/lesson/lesson_filter.html'




class Competition(NotManager, v.TemplateView):
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




class Calendar(NotManager, v.TemplateView):
	template_name = 'web/calendar/calendar.html'

	



class CalendarFilter(Calendar):
	template_name = 'web/calendarWWW/calendar_filter.html'




class BagtsView(NotManager, g.FormView):
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


class CompetitionRegisterView(NotManager, user_v.LoginRequired, g.FormView):
	template_name = "web/competition/competition_register.html"
	form_class = f.CompetitionRegisterForm
	success_url = reverse_lazy('web:competition')

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionRegisterView, self).get_context_data(*args, **kwargs)
		return context

	def form_valid(self, form):
		obj = form.save()
		m.register("C", file = obj.reciept, competition_id = self.kwargs['pk'], user_id = self.request.user.id)
		return super(CompetitionRegisterView, self).form_valid(form)



class LessonMailView(NotManager, g.FormView):

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
