# -*- coding:utf-8 -*-

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate, login, logout
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import (FormView, TemplateView, ListView, CreateView, UpdateView)
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils.html import escape
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, send_mass_mail
from django.core.exceptions import PermissionDenied

from .forms import ManagerLoginForm, ManagerForm, ManagerUpdateForm
from .models import Manager
from app.competition.models import CompetitionRank, Competition, CompetitionRegister
from app.competition.forms import *
from app.web.models import *
from app.web.forms import *
from app.user.models import SystemUser
from app.online_support.models import Support, SupportMessage
from app.online_support.forms import SupportManagerMessageForm

from django_modalview.generic.base import ModalTemplateView
from django_modalview.generic.edit import ModalFormView, ModalCreateView, ModalUpdateView
from django_modalview.generic.component import ModalResponse, ModalButton
from django_modalview.generic.response import ModalJsonResponseRedirect

__all__ = ['ManagerLoginView','ManagerHomeView', 'ManagerRankCreateView',
	'ManagerCompetitionCreateView', 'ManagerRankUpdateView', 'ManagerCompetitionUpdateView',
	'ManagerRankListView', 'ManagerCompetitionListView', 'ManagerNewsView', 'ManagerNewsCreateView',
	'ManagerNewsUpdateView', 'ManagerNewsCategoryCreateView', 'ManagerNewsCategoryUpdateView',
	'ManagerAboutView', 'ManagerAboutCreateView', 'ManagerLessonView', 'ManagerLessonCreateView',
	'ManagerLessonUpdateView', 'ManagerResearchView', 'ManagerResearchCreateView', 'ManagerResearchUpdateView',
	'ManagerUserListView', 'MyModal', 'MyModalUpdate', 'ManagerCompetitionRankCreateView',
	'ManagerCompetitionRankUpdateView', 'ManagerLessonCategoryUpdateView', 'ManagerLessonCategoryCreateView',
	'ManagerResearchCategoryUpdateView', 'ManagerResearchCategoryCreateView', 'ManagerCompetitionRegisterView',
	'manager_competition_register_view', 'ManagerAdminUserListView', 'ManagerAdminUserCreateView',
	'ManagerAdminUserUpdateView', 'ManagerFinanceView', 'ManagerSupportMessageView',
	'manager_support_message_view']


class PopupCreate(object):

	def form_valid(self, form):
		model = form.save(commit=False)
		form.save()
		if "_popup" in self.request.POST:
			return HttpResponse('<script>opener.dismissAddRelatedObjectPopup(window, "%s", "%s");</script>'\
				% (escape(model.pk), escape(model)))

class PopupUpdate(object):
	
	def form_valid(self, form):
		model = form.save(commit = False)
		form.save()
		if "_popup" in self.request.POST:
			return HttpResponse('<script>opener.dismissChangeRelatedObjectPopup(window, "%s", "%s", "%s");</script>'\
				% (escape(model.pk), escape(model), escape(model.pk)))

class MyModal(ModalCreateView):
	def __init__(self, *args, **kwargs):
		super(MyModal, self).__init__(*args, **kwargs)
		self.title = "Тэмцээний ангилал"
		self.form_class = CompetitionRankForm
		self.submit_button = ModalButton(value=u'Хадгалах', loading_value = "Уншиж байна...",
			button_type='success btn-flat')
		self.close_button = ModalButton(value=u'Хаах', button_type ='default btn-flat')

	def form_valid(self, form, **kwargs):
		#self.response = ModalResponse('Амжилттай хадгалагдлаа', 'success')
		#form.save()
		self.save(form)
		self.response = ModalResponse("{obj} is created".format(obj=self.object), 'success')
		return super(MyModal, self).form_valid(form, commit = False, **kwargs)

class MyModalUpdate(ModalUpdateView):
	def __init__(self, *args, **kwargs):
		super(MyModalUpdate, self).__init__(*args, **kwargs)
		self.title = "Тэмцээний ангилал"
		self.form_class = CompetitionRankForm
		self.submit_button = ModalButton(value=u'Хадгалах', loading_value = "Уншиж байна...",
			button_type='success btn-flat')
		self.close_button = ModalButton(value=u'Хаах', button_type ='default btn-flat')

	def dispatch(self, request, *args, **kwargs):
		self.object = CompetitionRank.objects.get(pk=kwargs.get('pk'))
		return super(MyModalUpdate, self).dispatch(request, *args, **kwargs)


	def form_valid(self, form, **kwargs):
		self.save(form)
		self.response = ModalResponse("{obj} амжилттай шинэчлэгдлээ".format(obj=self.object), 'success')
		return super(MyModalUpdate, self).form_valid(form, commit = False, **kwargs)

class ManagerLoginView(FormView):
	form_class = ManagerLoginForm
	template_name = 'manager/login.html'
	success_url = reverse_lazy('manager:manager_home')

	def get_success_url(self):
		return reverse_lazy('manager:manager_home')

	def dispatch(self, request, *args, **kwargs):
		if Manager.objects.filter(username = request.user.username):
			return HttpResponseRedirect(reverse_lazy('manager:manager_home'))
		return super(ManagerLoginView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
		if user and Manager.objects.filter(username = user.username):
			self.request.user = Manager.objects.get(username = user.username)
			login(self.request, user)
			url = self.request.GET.get('next', None)
			if url:
				return HttpResponseRedirect(url)
		return super(ManagerLoginView, self).form_valid(form)

	@staticmethod
	def logout(request):
		logout(request)
		return HttpResponseRedirect(reverse_lazy('manager:manager_login'))

class ManagerLoginRequired(object):
	get_perm = 'permission_denied'
	model = None

	@method_decorator(login_required(login_url = reverse_lazy('manager_login')))
	def dispatch(self, request, *args, **kwargs):
		user = request.user
		if user.is_authenticated():
			if Manager.objects.filter(username = user.username):
				if self.get_permissions(self.get_perm, self.model):
					return super(ManagerLoginRequired, self).dispatch(request, *args, **kwargs)
				else:
					raise PermissionDenied
		return HttpResponseRedirect(reverse_lazy('manager:manager_login'))

	def get_permissions(self, perm, model = None):
		perm_list = []
		user = self.request.user
		if model:
			for i in self.model._meta.default_permissions:
				i += "_"+self.model._meta.model_name
				perm_list.append(i)
		else:
			perm_list.append(perm)
		for i in user.groups.all():
			if i.permissions.filter(codename__in = perm_list):
				return True
		return False

class ManagerMessage(object):

	def get_context_data(self, *args, **kwargs):
		context = super(ManagerMessage, self).get_context_data(*args, **kwargs)
		context['messages'] = SupportMessage.objects.filter(
			support__manager__id = self.request.user.id,
			read_at = None,
			manager_message = None
			).order_by('-support_date')
		return context

class ManagerLoginNotPermissions(ManagerLoginRequired):

	def get_permissions(self, *args, **kwargs):
		return True

class ManagerHomeView(ManagerMessage, ManagerLoginNotPermissions, TemplateView):
	template_name = 'manager/home.html'


class ManagerRankListView(ManagerLoginRequired, ListView):
	model = CompetitionRank
	template_name = 'manager/rank/rank_list.html'

class ManagerRankCreateView(ManagerLoginRequired, CreateView):
	model = CompetitionRank
	form_class = CompetitionRankForm
	template_name = 'manager/rank/rank_form.html'
	success_url = reverse_lazy('manager_rank_list')

class ManagerRankUpdateView(ManagerLoginRequired, UpdateView):
	model = CompetitionRank
	form_class = CompetitionRankForm
	template_name = 'manager/rank/rank_form.html'
	success_url = reverse_lazy('manager_rank_list')


''' Тэмцээний crud view '''
class ManagerCompetitionListView(ManagerLoginRequired, ListView):
	model = Competition
	template_name = 'manager/competition/competition_list.html'

class ManagerCompetitionCreateView(ManagerLoginRequired, CreateView):
	model = Competition
	form_class = CompetitionForm
	template_name = 'manager/competition/competition_form.html'
	success_url = reverse_lazy('manager_competition')

class ManagerCompetitionUpdateView(ManagerLoginRequired, UpdateView):
	model = Competition
	form_class = CompetitionForm
	template_name = 'manager/competition/competition_form.html'
	success_url = reverse_lazy('manager_competition')

	def dispatch(self, request, *args, **kwargs):
		self.object = self.model.objects.get(id = self.kwargs['pk'])
		if self.object.started():
			raise Http404
		return super(ManagerCompetitionUpdateView, self).dispatch(request, *args, **kwargs)

class ManagerCompetitionRankCreateView(PopupCreate, ManagerLoginRequired, CreateView):
	model = CompetitionRank
	form_class = CompetitionRankForm
	template_name = 'manager/competition/competition_rank_form.html'
	success_url = reverse_lazy('manager_competition')

class ManagerCompetitionRankUpdateView(PopupUpdate, ManagerLoginRequired, UpdateView):
	model = CompetitionRank
	form_class = CompetitionRankForm
	template_name = 'manager/competition/competition_rank_form.html'
	success_url = reverse_lazy('manager_competition')
''' Төгсгөл тэмцээний crud view '''

class ManagerNewsView(ManagerLoginRequired, ListView):
	model = Medee
	template_name = 'manager/news/news_list.html'

class ManagerNewsCreateView(ManagerLoginRequired, CreateView):
	model = Medee
	form_class = NewsForm
	template_name = 'manager/news/news_form.html'
	success_url = reverse_lazy('manager_news')

	def form_valid(self, form):
		news = form.save()
		mails = []
		for i in SystemUser.objects.all():
			mails.append(i.email)
		message = ('no reply', news.title, 'uuganaaaaaa@gmail.com', mails)
		send_mass_mail((message,))
		return super(ManagerNewsCreateView, self).form_valid(form)

class ManagerNewsUpdateView(ManagerLoginRequired, UpdateView):
	model = Medee
	form_class = NewsForm
	template_name = 'manager/news/news_form.html'
	success_url = reverse_lazy('manager_news')

class ManagerNewsCategoryCreateView(PopupCreate, ManagerLoginRequired, CreateView):
	model = MedeeAngilal
	form_class = NewsCategoryForm
	success_url = reverse_lazy('manager_news')
	template_name = "manager/news/news_category_form.html"

class ManagerNewsCategoryUpdateView(PopupUpdate, ManagerLoginRequired, UpdateView):
	model = MedeeAngilal
	form_class = NewsCategoryForm
	success_url = reverse_lazy('manager_news')
	template_name = "manager/news/news_category_form.html"

class ManagerAboutView(ManagerLoginRequired, TemplateView):
	model = BidniiTuhai
	template_name = 'manager/about/about.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ManagerAboutView, self).get_context_data(*args, **kwargs)
		context['about'] = BidniiTuhai.objects.first()
		return context

class ManagerAboutCreateView(ManagerLoginRequired, FormView):
	model = BidniiTuhai
	form_class = AboutForm
	template_name = 'manager/about/about_create.html'
	success_url = reverse_lazy('manager_about')
	def dispatch(self, request, *args, **kwargs):
		self.model = BidniiTuhai.objects.first()
		return super(ManagerAboutCreateView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		if self.model:
			self.model.body = form.cleaned_data['body']
			self.model.video_url = form.cleaned_data['video_url']
			self.model.save()
		else:
			form.save()
		return super(ManagerAboutCreateView, self).form_valid(form)

	def get_initial(self):
		initial = super(ManagerAboutCreateView, self).get_initial()
		if self.model:
			initial['body'] = self.model.body
			initial['video_url'] = self.model.video_url
		else:
			pass
		return initial

class ManagerLessonView(ManagerLoginRequired, ListView):
	model = Surgalt
	template_name = 'manager/lesson/lesson_list.html'

class ManagerLessonCreateView(ManagerLoginRequired, CreateView):
	model = Surgalt
	form_class = LessonForm
	template_name = 'manager/lesson/lesson_form.html'
	success_url = reverse_lazy('manager_lesson')

class ManagerLessonUpdateView(ManagerLoginRequired, UpdateView):
	model = Surgalt
	form_class = LessonForm
	success_url = reverse_lazy('manager_lesson')
	template_name = 'manager/lesson/lesson_form.html'

class ManagerLessonCategoryCreateView(PopupCreate, ManagerLoginRequired, CreateView):
	model = SurgaltAngilal
	form_class = LessonCategoryForm
	template_name = 'manager/lesson/lesson_category_form.html'
	success_url = reverse_lazy('manager_competition')

class ManagerLessonCategoryUpdateView(PopupUpdate, ManagerLoginRequired, UpdateView):
	model = SurgaltAngilal
	form_class = LessonCategoryForm
	template_name = 'manager/lesson/lesson_category_form.html'
	success_url = reverse_lazy('manager_competition')



class ManagerResearchView(ManagerLoginRequired, ListView):
	model = Sudalgaa
	template_name = 'manager/research/research_list.html'

class ManagerResearchCreateView(ManagerLoginRequired, CreateView):
	model = Sudalgaa
	form_class = ResearchForm
	template_name = 'manager/research/research_form.html'
	success_url = reverse_lazy('manager_research')
	
class ManagerResearchUpdateView(ManagerLoginRequired, UpdateView):
	model = Sudalgaa
	form_class = ResearchForm
	success_url = reverse_lazy('manager_research')
	template_name = 'manager/research/research_form.html'

class ManagerResearchCategoryCreateView(PopupCreate, ManagerLoginRequired, CreateView):
	model = SudalgaaAngilal
	form_class = ResearchCategoryForm
	template_name = 'manager/research/research_category_form.html'
	success_url = reverse_lazy('manager_competition')

class ManagerResearchCategoryUpdateView(PopupUpdate, ManagerLoginRequired, UpdateView):
	model = SudalgaaAngilal
	form_class = ResearchCategoryForm
	template_name = 'manager/research/research_category_form.html'
	success_url = reverse_lazy('manager_competition')
	
class ManagerUserListView(ManagerLoginRequired, ListView):
	model = SystemUser
	template_name = 'manager/user/user.html'

class ManagerAdminUserListView(ManagerLoginRequired, ListView):
	model = Manager
	template_name = 'manager/user/admin/admin_user_list.html'

class ManagerAdminUserCreateView(ManagerLoginRequired, CreateView):
	model = Manager
	form_class = ManagerForm
	template_name = 'manager/user/admin/admin_user_form.html'
	success_url = reverse_lazy('manager_admin_user_list')

	def form_valid(self, form):
		user = form.save()
		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		text = 'http://127.0.0.1:8000/confirm/%s/%s/' %(uid, token)
		send_mail('subject', text, 'uuganaaaaaa@gmail.com', [user.email])
		context = {}
		context['email'] = user.email
		return super(ManagerAdminUserCreateView, self).form_valid(form)

class ManagerAdminUserUpdateView(ManagerLoginRequired, UpdateView):
	model = Manager
	form_class = ManagerUpdateForm
	template_name = 'manager/user/admin/admin_user_form.html'
	success_url = reverse_lazy('manager_admin_user_list')
	
# End Temtseen crud

class ManagerCompetitionRegisterView(ManagerLoginRequired, ListView):
	model = CompetitionRegister
	queryset = CompetitionRegister.objects.filter(status = False)
	template_name = 'manager/competition/competition_register.html'

def manager_competition_register_view(request, id = 0):
	competition_register = CompetitionRegister.objects.get(id = id)
	competition_register.status = True
	competition_register.save()
	#send_mail(
	#	'no-reply',
	#	'Тэмцээнд нэвтрэх нэр: %s' %(competition_register.account),
	#	'uuganaaaaaa@gmail.com',
	#	[competition_register.user.email]
	#	)
	from notifications.signals import notify
	notify.send(request.user, recipient=request.user, verb='you reached level 10')
	return HttpResponseRedirect(reverse_lazy('manager:manager_competition_register'))

class ManagerFinanceView(ManagerLoginRequired, TemplateView):
	get_perm = 'add_medee'
	template_name = 'manager/finance/finance.html'

class ManagerSupportMessageView(ManagerLoginRequired, CreateView):

	model = SupportMessage
	form_class = SupportManagerMessageForm
	template_name = 'manager/support_message/support_message_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ManagerSupportMessageView, self).get_context_data(*args, **kwargs)
		context['object_list'] = SupportMessage.objects.filter(
			support__system_user__id = self.kwargs['id'],
			support__manager__id = self.request.user.id
		)
		return context

	def form_valid(self, form):
		manager = Manager.objects.get(id = self.request.user.id)
		system_user = SystemUser.objects.get(id = self.kwargs['id'])
		if not Support.objects.filter(manager = manager, system_user = system_user):
			message = Support.objects.create(manager = manager, system_user = system_user)
		else:
			message = Support.objects.get(manager = manager, system_user = system_user)
		model = form.save(commit = False)
		model.support = message
		model.save()
		res = {
			'id': model.id,
			'msg': model.manager_message,
			'user': model.support.manager.username,
			'time': model.support_date.strftime('%I:%M:%S %p').lstrip('0')
			}
		data = json.dumps(res)
		return HttpResponse(data,content_type="application/json")

def manager_support_message_view(request, id = 0):
	messages = SupportMessage.objects.filter(
		support__manager__id = request.user.id,
		support__system_user__id = id
		)
	c = []
	for m in messages:
		c.append({
			'manager': m.support.manager.username ,
			'user': m.support.system_user.username,
			'manager_msg': m.manager_message,
			'user_msg': m.system_user_message,
			'time': m.support_date.strftime('%I:%M:%S %p').lstrip('0')
		}) 
	data = json.dumps(c)
	return HttpResponse(data, content_type="application/json")