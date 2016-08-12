# -*- coding:utf-8 -*-
from datetime import datetime, date, timedelta
from django.views.generic import TemplateView, FormView, ListView, CreateView, View
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.template import RequestContext
from .forms import BagtsForm, LessonMailForm
from .models import *
from app.competition.models import *
from app.competition.forms import CompetitionRegisterForm
from app.user.models import SystemUser, Bank
from app.manager.models import Manager
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

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			if SystemUser.objects.filter(username = request.user.username):
				return super(SystemUserLoginRequired, self).dispatch(request, *args, **kwargs)
			else:
				return HttpResponseRedirect(reverse_lazy('web:login'))
		else:
			return HttpResponseRedirect(reverse_lazy('web:login'))


class NotManager(object):

	def dispatch(self, request, *args, **kwargs):
		if not Manager.objects.filter(username = request.user.username):
			return super(NotManager, self).dispatch(request, *args, **kwargs)
		else:
			return HttpResponseRedirect(reverse_lazy('user:login'))


class Web(NotManager):

	def get_context_data(self, *args, **kwargs):
		
		context = super(Web, self).get_context_data(*args, **kwargs)
		#context['corausel'] = Medee.objects.all().order_by('created_at')[:5]
		#context['news_category'] = MedeeAngilal.objects.all()
		#context['research_category'] = SudalgaaAngilal.objects.all()
		#context['lesson_category'] = SurgaltAngilal.objects.all()
		#context['medee'] = Medee.objects.all().order_by('-id')[:5]
		#context['medee_most'] = Medee.objects.all().order_by('-view')[:5]
		#context['sudalgaa'] = Sudalgaa.objects.all().order_by('-id')[:5]
		#context['surgalt'] = Surgalt.objects.all()[:4]
		#context['menu_num'] = self.menu_num
		return context


class Home(NotManager, FormView):
	template_name = 'web/home/home_example.html'
	form_class = RegisterForm
	success_url = reverse_lazy('home')

	#def dispatch(self, request, *args, **kwargs):
		#from datetime import datetime
		#a = datetime.now()
		#print c.check_token(1 ,2 , 3, a, 'MQ-Mg-Mw-NTY1Mw')
		#print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		#return super(Home, self).dispatch(request, *args, **kwargs)
	
	def get_context_data(self, *args, **kwargs):
		context = super(Home, self).get_context_data(*args, **kwargs)
		context['news_first'] = Medee.objects.first()
		context['research_first'] = Sudalgaa.objects.first()
		context['lesson_first'] = Surgalt.objects.first()
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
		context['about'] = BidniiTuhai.objects.last()
		return context

class News(Web, TemplateView):
	template_name = 'web/news/news.html'
	menu_num = 4

class NewsSelf(Web, TemplateView):
	template_name = 'web/news/news_self.html'

	def get_context_data(self, *args, **kwargs):
		context = super(NewsSelf, self).get_context_data(*args, **kwargs)
		#context['news_self'] = Medee.objects.get(id = self.kwargs.pop('id', None))
		context['news_self'].view += 11
		#context['news_self'].save(update_fields=['view'])
		return context


class Research(SystemUserLoginRequired, Web, TemplateView):
	template_name = 'web/research/research.html'

	def get_context_data(self, **kwargs):
		context = super(Research, self).get_context_data(**kwargs)
		name = self.request.GET.get('name', None)
		author_name = self.request.GET.get('author_name', None)
		if name and author_name:
			object_list = Sudalgaa.objects.filter(name__icontains = name, author_name__icontains = author_name)
		elif name:
			object_list = Sudalgaa.objects.filter(name__icontains = name)
		elif author_name:
			object_list = Sudalgaa.objects.filter(author_name__icontains = author_name)
		else:
			object_list = Sudalgaa.objects.all()
		category_list = []
		for i in object_list.values('angilal').distinct():
			obj = SudalgaaAngilal.objects.get(id = i.values()[0])
			setattr(obj, 'research_list', [])
			category_list.append(obj)
			for ob in object_list:
				if ob.angilal.id == obj.id:
					obj.research_list.append(ob)
		context['research_category'] = category_list
		return context


class ResearchFilter(Research):
	template_name = 'web/research/research_filter.html'


class Lesson(Web, ListView):
	template_name = 'web/lesson/lesson.html'
	#model = Surgalt

	def get_context_data(self, *args, **kwargs):
		context = super(Lesson, self).get_context_data(*args, **kwargs)
		name = self.request.GET.get('name', None)
		if name:
			object_list = Surgalt.objects.filter(video_name__icontains = name)
		else:
			object_list = Surgalt.objects.all()
		lesson_category_list = []
		for i in object_list.values('angilal').distinct():
			obj = SurgaltAngilal.objects.get(id = i.values()[0])
			setattr(obj, 'lesson_list', [])
			lesson_category_list.append(obj)
			for ob in object_list:
				if ob.angilal.id == obj.id:
					obj.lesson_list.append(ob)
		context['lesson_category'] = lesson_category_list
		return context


class LessonFilter(Lesson):
	template_name = 'web/lesson/lesson_filter.html'


class Contact(Web, TemplateView):

	template_name = 'web/contact.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Contact, self).get_context_data(*args, **kwargs)
		context['contact'] = HolbooBarih.objects.last()
		return context


class WebCompetitionCalendar(Web, ListView):
	template_name = 'web/competition/competition.html'
	model = Competition

	def get_context_data(self, *args, **kwargs):
		context = super(WebCompetitionCalendar, self).get_context_data(*args, **kwargs)
		filter_type = self.request.GET.get('filter_type', None)
		start = self.request.GET.get('start', None)
		end = self.request.GET.get('end', None)
		if filter_type == '0':
			object_list = Competition.objects.all()
		elif filter_type == '1':
			object_list = Competition.registered_competition(self.request.user)
		elif filter_type == '2':
			object_list = Competition.objects.filter(competition_status = 0)
		elif filter_type == '3':
			object_list = Competition.objects.filter(competition_status = 1)
		elif filter_type == '4':
			object_list = Competition.objects.filter(competition_status = 2)
		elif filter_type == '5':
			start = datetime.strptime(start, '%Y-%m-%d').replace(hour=0, minute=0)
			end = datetime.strptime(end, '%Y-%m-%d').replace(hour=0, minute=0)
			if start == end:
				object_list = Competition.objects.filter(start__startswith = start.date())
			else:
				object_list = Competition.objects.filter(start__range = (start, end))
		else:
			object_list = Competition.objects.all()
		context['object_list'] = object_list
		return context


class WebCompetitionCalendarFilter(WebCompetitionCalendar):
	template_name = 'web/competition/competition_filter.html'


class Contact(Web, TemplateView):
	template_name = 'web/contact.html'


class Calendar(Web, TemplateView):
	template_name = 'web/calendar/calendar.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Calendar, self).get_context_data(*args, **kwargs)
		filter_type = self.request.GET.get('filter', None)
		start = self.request.GET.get('start', None)
		end = self.request.GET.get('end', None)
		if filter_type:
			if filter_type == '1':
				object_list = EconomicCalendar.objects.filter(time__startswith = date.today() - timedelta(1))
			elif filter_type == '2':
				object_list = EconomicCalendar.objects.filter(time__startswith = date.today())
			elif filter_type == '3':
				object_list = EconomicCalendar.objects.filter(time__startswith = date.today() + timedelta(1))
			elif filter_type == '4':
				object_list = EconomicCalendar.objects.filter(time__range =
					(date.today(), date.today() + timedelta(7))).order_by('time')
			elif filter_type == '0':
				start = datetime.strptime(start, '%Y-%m-%d').replace(hour=0, minute=0)
				end = datetime.strptime(end, '%Y-%m-%d').replace(hour=0, minute=0)
				if start == end:
					print start
					object_list = EconomicCalendar.objects.filter(time__startswith = start.date()).order_by('time')
				else:
					object_list = EconomicCalendar.objects.filter(time__range = (start.date(), end.date())).order_by('time')
		else:
			object_list = EconomicCalendar.objects.filter(time__startswith = date.today())
		context['object_list'] = object_list
		return context


class CalendarFilter(Calendar):
	template_name = 'web/calendar/calendar_filter.html'


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
		user = SystemUser.objects.get(id = self.kwargs.pop('user_id', None))
		video = Surgalt.objects.get(id = self.kwargs.pop('video_id', None))
		message += user.email
		try:
			email = EmailMessage(subject, message, to = [video.author_email])
			email.send()
		except BadHeaderError:
			return HttpResponse('Амжилтгүй')
		return super(LessonMailView, self).form_valid(form, **kwargs)
