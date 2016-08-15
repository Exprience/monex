# -*- coding:utf-8 -*-
from datetime import datetime, date, timedelta
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.template import RequestContext
from .forms import BagtsForm, LessonMailForm
from app.competition.forms import CompetitionRegisterForm
from app.user.forms import RegisterForm

from django_modalview.generic.base import ModalTemplateView
from django_modalview.generic.edit import ModalFormView, ModalCreateView, ModalUpdateView
from django_modalview.generic.component import ModalResponse, ModalButton
from django_modalview.generic.response import ModalJsonResponseRedirect

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from app.competition.token import competition_register_token as c


__all__ = [
	'Home', 'About', 'News', 'Research', 'Lesson', 'Contact', 'NewsSelf',
	'WebCompetitionCalendar', 'Calendar', 'BagtsView', 'WebCompetitionRegisterView', 'CalendarFilter',
	'ResearchFilter', 'LessonMailView', 'WebCompetitionCalendarFilter', 'LessonFilter','handler404',
	'handler500'
	]


def handler404(request):
	template = 'web/handler/404.html'
	if not SystemUser.objects.filter(id = request.user.id):
		template = 'manager/handler/404.html'

	response = render_to_response(template, {},
                                  context_instance=RequestContext(request))
	response.status_code = 404
	return response


def handler500(request):
    response = render_to_response('web/handler/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


class SystemUserLoginRequired(object):
	pass


class NotManager(object):

	pass


class Web():

	def get_context_data(self, *args, **kwargs):
		
		context = super(Web, self).get_context_data(*args, **kwargs)
		return context


class Home(FormView):
	template_name = 'web/home/home_example.html'
	form_class = RegisterForm
	success_url = reverse_lazy('home')

	
	def get_context_data(self, *args, **kwargs):
		context = super(Home, self).get_context_data(*args, **kwargs)
		return context

	def form_valid(self, form):
		user = form.save()
		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		text = 'http://127.0.0.1:8000/reset/%s/%s/' %(uid, token)
		send_mail('subject', text, 'uuganaaaaaa@gmail.com', [user.email])
		messages.success(self.request,
			u'Бүртгэл амжилттай хийгдлээ. %s мэйл хаяг руу орж бүртгэлээ баталгаажуулна уу.' %user.email)
		return super(Home, self).form_valid(form)

	def form_invalid(self, form):
		messages.error(self.request, 'Бүртгүүлэх формд алдаа гарлаа')
		return super(Home, self).form_invalid(form)


class About(Web, TemplateView):
	template_name = 'web/about.html'

	def get_context_data(self, *args, **kwargs):
		context = super(About, self).get_context_data(*args, **kwargs)
		return context

class News(Web, TemplateView):
	template_name = 'web/news/news.html'
	menu_num = 4

class NewsSelf(Web, TemplateView):
	template_name = 'web/news/news_self.html'

	def get_context_data(self, *args, **kwargs):
		context = super(NewsSelf, self).get_context_data(*args, **kwargs)
		return context


class Research(SystemUserLoginRequired, Web, TemplateView):
	template_name = 'web/research/research.html'

	def get_context_data(self, **kwargs):
		context = super(Research, self).get_context_data(**kwargs)
		return context


class ResearchFilter(Research):
	template_name = 'web/research/research_filter.html'


class Lesson(Web, FormView):
	template_name = 'web/lesson/lesson.html'
	#model = Surgalt

	def get_context_data(self, *args, **kwargs):
		context = super(Lesson, self).get_context_data(*args, **kwargs)
		return context


class LessonFilter(Lesson):
	template_name = 'web/lesson/lesson_filter.html'


class Contact(Web, TemplateView):

	template_name = 'web/contact.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Contact, self).get_context_data(*args, **kwargs)
		context['contact'] = HolbooBarih.objects.last()
		return context


class WebCompetitionCalendar(Web, TemplateView):
	template_name = 'web/competition/competition.html'

	def get_context_data(self, *args, **kwargs):
		context = super(WebCompetitionCalendar, self).get_context_data(*args, **kwargs)
		return context


class WebCompetitionCalendarFilter(WebCompetitionCalendar):
	template_name = 'web/competition/competition_filter.html'


class Contact(Web, TemplateView):
	template_name = 'web/contact.html'


class Calendar(Web, TemplateView):
	template_name = 'web/calendar/calendar.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Calendar, self).get_context_data(*args, **kwargs)
		return context


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


class WebCompetitionRegisterView(SystemUserLoginRequired, ModalFormView):

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
