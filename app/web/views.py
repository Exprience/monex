#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime, date, timedelta


from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages


from django_modalview.generic.base import ModalTemplateView
from django_modalview.generic.edit import ModalFormView, ModalCreateView, ModalUpdateView
from django_modalview.generic.component import ModalResponse, ModalButton
from django_modalview.generic.response import ModalJsonResponseRedirect


#from app.competition.token import competition_register_token as c
from app.user.views import UserLoginRequired
from .forms import BagtsForm, LessonMailForm
from app.competition.forms import CompetitionRegisterForm


#Exports
__all__ = []




class Home(TemplateView):
	template_name = 'web/home/home.html'




class News(TemplateView):
	template_name = 'web/news/news.html'




class NewsSelf(TemplateView):
	template_name = 'web/news/news_self.html'




class Research(UserLoginRequired, TemplateView):
	template_name = 'web/research/research.html'




class ResearchFilter(Research):
	template_name = 'web/research/research_filter.html'




class Lesson(FormView):
	template_name = 'web/lesson/lesson.html'
	form_class = LessonMailForm




class LessonFilter(Lesson):
	template_name = 'web/lesson/lesson_filter.html'




class WebCompetitionCalendar(TemplateView):
	template_name = 'web/competition/competition.html'




class WebCompetitionCalendarFilter(WebCompetitionCalendar):
	template_name = 'web/competition/competition_filter.html'




class Calendar(TemplateView):
	template_name = 'web/calendar/calendar.html'




class CalendarFilter(Calendar):
	template_name = 'web/calendarWWW/calendar_filter.html'




class BagtsView(ModalFormView):
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




class WebCompetitionRegisterView(UserLoginRequired, ModalFormView):

	def __init__(self, *args, **kwargs):
		super(WebCompetitionRegisterView, self).__init__(*args, **kwargs)
		self.title = "Тэмцээний ангилал"
		self.form_class = CompetitionRegisterForm
		self.submit_button = ModalButton(value=u'Хадгалах', loading_value = "Уншиж байна...",
			button_type='success btn-flat')
		self.close_button = ModalButton(value=u'Хаах', button_type ='default btn-flat')

	def form_valid(self, form):
		object = form.save(commit = False)
		if SystemUser.objects.filter(username = self.request.user.username) and \
		Competition.objects.filter(id =self.kwargs['id']):	
			object.user = SystemUser.objects.get(username = self.request.user.username)
			object.competition = Competition.objects.get(id = self.kwargs.pop('id', None))
			object.auto_increment()
			object.save()
			#competition_register_token(object.user.id, object.account, )
			self.response = ModalResponse('Амжилттай хадгалагдлаа', 'success')
			return super(WebCompetitionRegisterView, self).form_valid(form)
		else:
			return super(WebCompetitionRegisterView, self).form_invalid(form)




class LessonMailView(ModalFormView):

	def __init__(self, *args, **kwargs):
		super(LessonMailView, self).__init__(*args, **kwargs)
		self.title = u"Санал хүсэлт"
		self.form_class = LessonMailForm
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
