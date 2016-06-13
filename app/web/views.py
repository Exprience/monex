# -*- coding:utf-8 -*-

from django.views.generic import TemplateView, FormView, ListView, CreateView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response

from .forms import BagtsForm
from .models import *
from app.competition.models import *
from app.competition.forms import CompetitionRegisterForm
from app.user.models import SystemUser
from app.manager.models import Manager

from django_modalview.generic.base import ModalTemplateView
from django_modalview.generic.edit import ModalFormView, ModalCreateView, ModalUpdateView
from django_modalview.generic.component import ModalResponse, ModalButton
from django_modalview.generic.response import ModalJsonResponseRedirect

__all__ = ['Home', 'About', 'News', 'Research', 'Lesson', 'Contact', 'NewsSelf',
'WebCompetitionCalendar', 'Calendar', 'h404', 'BagtsView', 'WebCompetitionRegisterView']



def h404(request):
    response = render_to_response('web/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('web/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

class SystemUserLoginRequired(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			if SystemUser.objects.filter(username = request.user.username):
				return super(SystemUserLoginRequired, self).dispatch(request, *args, **kwargs)
			else:
				return HttpResponseRedirect(reverse_lazy('login'))
		else:
			return HttpResponseRedirect(reverse_lazy('login'))

class NotManager(object):

	def dispatch(self, request, *args, **kwargs):
		if not Manager.objects.filter(username = request.user.username):
			return super(NotManager, self).dispatch(request, *args, **kwargs)
		else:
			return HttpResponseRedirect(reverse_lazy('login'))

class Web(NotManager):

	menu_num = 0

	def get_context_data(self, *args, **kwargs):
		context = super(Web, self).get_context_data(*args, **kwargs)
		context['corausel'] = Medee.objects.all().order_by('created_at')[:5]
		context['medee_angilal'] = MedeeAngilal.objects.all()
		context['sudalgaa_angilal'] = SudalgaaAngilal.objects.all()
		context['surgalt_angilal'] = SurgaltAngilal.objects.all()
		context['medee'] = Medee.objects.all().order_by('-id')[:5]
		context['medee_most'] = Medee.objects.all().order_by('-view')[:5]
		context['sudalgaa'] = Sudalgaa.objects.all().order_by('-id')[:5]
		context['surgalt'] = Surgalt.objects.all()[:4]
		context['menu_num'] = self.menu_num
		return context

class Home(Web, TemplateView):
	template_name = 'web/home.html'
	menu_num = 1

class About(Web, TemplateView):
	template_name = 'web/about.html'
	menu_num = 2

	def get_context_data(self, *args, **kwargs):
		context = super(About, self).get_context_data(*args, **kwargs)
		context['about'] = BidniiTuhai.objects.last()
		return context

class News(Web, ListView):
	template_name = 'web/news.html'
	menu_num = 4
	model = Medee

class NewsSelf(Web, TemplateView):
	template_name = 'web/news_self.html'
	menu_num = 4

	def get_context_data(self, *args, **kwargs):
		context = super(NewsSelf, self).get_context_data(*args, **kwargs)
		context['news_self'] = Medee.objects.get(id = self.kwargs.pop('id', None))
		context['news_self'].view += 1
		context['news_self'].save()
		return context

class Research(Web, TemplateView):
	template_name = 'web/research.html'
	menu_num = 5

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		self.sudalgaa_number = self.kwargs.pop('id', None)
		return super(Research, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(Research, self).get_context_data(*args, **kwargs)
		context['sudalgaa'] = Sudalgaa.objects.all() #filter(angilal__id = self.sudalgaa_number)
		#context['sudalgaa_number'] = int(self.sudalgaa_number)
		return context

class Lesson(Web, ListView):
	template_name = 'web/lesson.html'
	menu_num = 6
	model = Surgalt

class Contact(Web, TemplateView):

	template_name = 'web/contact.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Contact, self).get_context_data(*args, **kwargs)
		context['contact'] = HolbooBarih.objects.last()
		return context
	
class WebCompetitionCalendar(Web, ListView):
	menu_num = 3
	template_name = 'web/competition.html'
	model = Competition

class Contact(Web, TemplateView):
	menu_num = 9
	template_name = 'web/contact.html'

class Calendar(Web, TemplateView):
	menu_num = 7
	template_name = 'web/calendar.html'

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
			return super(WebCompetitionRegisterView, self).form_valid(form)
		else:
			return super(WebCompetitionRegisterView, self).form_invalid(form)