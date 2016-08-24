# -*- coding:utf-8 -*-

import json
from datetime import datetime
from django.template import Template, Context
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate, login, logout
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy, reverse
from django.views import generic as g
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils.html import escape
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, send_mass_mail
from django.core.exceptions import PermissionDenied
from django.utils.html import format_html
from django.utils.translation import ugettext as _

from .forms import ManagerLoginForm, ManagerForm, ManagerUpdateForm
from app.competition.forms import *
from app.web.forms import (NewsForm, NewsCategoryForm, LessonForm, LessonCategoryForm, ResearchForm, ResearchCategoryForm)
from app.online_support.forms import SupportManagerMessageForm


from django_modalview.generic import (
									edit as me, 
									base as mb,
									response as mr,
									component as mc)



#__all__ = [
#	'ManagerLoginView', 'ManagerHomeView', 'ManagerRankCreateView',
#	'ManagerCompetitionCreateView', 'ManagerRankUpdateView', 'ManagerCompetitionUpdateView',
#	'ManagerRankListView', 'ManagerCompetitionListView', 'ManagerNewsView', 'ManagerNewsCreateView',
#	'ManagerNewsUpdateView', 'ManagerNewsCategoryCreateView', 'ManagerNewsCategoryUpdateView',
#	'ManagerAboutView', 'ManagerAboutCreateView', 'ManagerLessonView', 'ManagerLessonCreateView',
#	'ManagerLessonUpdateView', 'ManagerResearchView', 'ManagerResearchCreateView', 'ManagerResearchUpdateView',
#	'ManagerUserListView', 'RankCreateModalView', 'RankUpdateModalView', 'ManagerCompetitionRankCreateView',
#	'ManagerCompetitionRankUpdateView', 'ManagerLessonCategoryUpdateView', 'ManagerLessonCategoryCreateView',
#	'ManagerResearchCategoryUpdateView', 'ManagerResearchCategoryCreateView', 'ManagerCompetitionRegisterView',
#	'manager_competition_register_view', 'ManagerAdminUserListView', 'ManagerAdminUserCreateView',
#	'ManagerAdminUserUpdateView', 'ManagerFinanceView', 'ManagerSupportMessageView',
#	'manager_support_message_view', 'ManagerCompetitionHistoryView', 'ManagerCompetitionFilter']


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



class ModalView(object):
	def __init__(self, *args, **kwargs):
		super(ModalView, self).__init__(*args, **kwargs)
		self.title = u"Тэмцээний ангилал"
		self.form_class = CompetitionRankForm
		self.submit_button = mc.ModalButton(value=u'Хадгалах', loading_value = "Уншиж байна...",
			button_type='success btn-flat')
		self.close_button = mc.ModalButton(value=u'Хаах', button_type ='default btn-flat')

class RankCreateModalView(ModalView, me.ModalCreateView):

	def __init__(self, *args, **kwargs):
		super(RankCreateModalView, self).__init__(*args, **kwargs)
		self.title = u"Тэмцээний ангилал нэмэх"

	def form_valid(self, form, **kwargs):
		return super(RankCreateModalView, self).form_valid(form, commit = False, **kwargs)

class RankUpdateModalView(ModalView, me.ModalUpdateView):



	def form_valid(self, form, **kwargs):
		self.save(form)
		self.response = mc.ModalResponse("{obj} амжилттай шинэчлэгдлээ".format(obj=self.object), 'success btn-flat')
		return super(RankUpdateModalView, self).form_valid(form, commit = False, **kwargs)







class ManagerLoginView(g.FormView):
	form_class = ManagerLoginForm
	template_name = 'manager/login.html'
	success_url = reverse_lazy('manager:manager_home')

	def get_success_url(self):
		return reverse_lazy('manager:manager_home')

	def dispatch(self, request, *args, **kwargs):
		return super(ManagerLoginView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		return super(ManagerLoginView, self).form_valid(form)

	@staticmethod
	def logout(request):
		return HttpResponseRedirect(reverse_lazy('manager:manager_login'))

class ManagerLoginRequired(object):
	pass
	#get_perm = 'permission_denied'
	#model = None

	#@method_decorator(login_required(login_url = reverse_lazy('manager:manager_login')))
	#def dispatch(self, request, *args, **kwargs):
	#	user = request.user
	#	if user.is_authenticated():
	#		if Manager.objects.filter(username = user.username):
	#			if self.get_permissions(self.get_perm, self.model):
	#				return super(ManagerLoginRequired, self).dispatch(request, *args, **kwargs)
	#			else:
	#				raise PermissionDenied
	#	return HttpResponseRedirect(reverse_lazy('manager:manager_login'))

	#def get_permissions(self, perm, model = None):
	#	perm_list = []
	#	user = self.request.user
	#	if model:
	#		for i in self.model._meta.default_permissions:
	#			i += "_"+self.model._meta.model_name
	#			perm_list.append(i)
	#	else:
	#		perm_list.append(perm)
	#	for i in user.groups.all():
	#		if i.permissions.filter(codename__in = perm_list):
	#			return True
	#	return False

class ManagerMessage(object):

	def get_context_data(self, *args, **kwargs):
		context = super(ManagerMessage, self).get_context_data(*args, **kwargs)
		return context

class ManagerLoginNotPermissions(ManagerLoginRequired):

	def get_permissions(self, *args, **kwargs):
		return True

class ManagerHomeView(ManagerMessage, ManagerLoginNotPermissions, g.TemplateView):
	template_name = 'manager/home.html'






''' Тэмцээний ангилал crud view '''

class ManagerRankListView(ManagerLoginRequired, g.TemplateView):
	template_name = 'manager/rank/rank_list.html'

class ManagerRankCreateView(ManagerLoginRequired, g.FormView):
	form_class = CompetitionRankForm
	template_name = 'manager/rank/rank_form.html'
	success_url = reverse_lazy('manager_rank_list')

class ManagerRankUpdateView(ManagerLoginRequired, g.FormView):
	form_class = CompetitionRankForm
	template_name = 'manager/rank/rank_form.html'
	success_url = reverse_lazy('manager_rank_list')

''' Төгсгөл тэмцээний ангилал crud view '''






''' Тэмцээний crud view '''

class ManagerCompetitionListView(ManagerLoginRequired, g.TemplateView):
	template_name = 'manager/competition/competition_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ManagerCompetitionListView, self).get_context_data(*args, **kwargs)
		return context

class ManagerCompetitionCreateView(ManagerLoginRequired, g.FormView):
	form_class = CompetitionForm
	template_name = 'manager/competition/competition_form.html'
	success_url = reverse_lazy('manager_competition')

class ManagerCompetitionUpdateView(ManagerLoginRequired, g.FormView):
	form_class = CompetitionForm
	template_name = 'manager/competition/competition_form.html'
	success_url = reverse_lazy('manager_competition')


class ManagerCompetitionRankCreateView(PopupCreate, ManagerLoginRequired, g.FormView):
	form_class = CompetitionRankForm
	template_name = 'manager/competition/competition_rank_form.html'
	success_url = reverse_lazy('manager_competition')

class ManagerCompetitionRankUpdateView(PopupUpdate, ManagerLoginRequired, g.FormView):
	form_class = CompetitionRankForm
	template_name = 'manager/competition/competition_rank_form.html'
	success_url = reverse_lazy('manager_competition')

class ManagerCompetitionHistoryView(ManagerLoginNotPermissions, mb.ModalTemplateView):

	def __init__(self, *args, **kwargs):
		super(ManagerCompetitionHistoryView, self).__init__(*args, **kwargs)
		from django.template import loader
		a = loader.get_template('manager/competition/competition_list.html')
		self.title = u"Түүх"
		self.description = "fasdfasdf" #t
		self.icon = "icon-mymodal"
		self.close_button = mc.ModalButton(value=u'Хаах', button_type ='default btn-flat')

class ManagerCompetitionFilter(ManagerLoginNotPermissions, g.TemplateView):
	template_name = 'manager/competition/competition_filter.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ManagerCompetitionFilter, self).get_context_data(*args, **kwargs)
		return context

''' Төгсгөл тэмцээний crud view '''






class ManagerNewsView(ManagerLoginRequired, g.TemplateView):
	template_name = 'manager/news/news_list.html'

class ManagerNewsCreateView(ManagerLoginRequired, g.FormView):
	form_class = NewsForm
	template_name = 'manager/news/news_form.html'
	success_url = reverse_lazy('manager:manager_news')

	def form_valid(self, form):
		news = form.save(commit = False)
		#news.created_by = SystemUser.objects.get(id = self.request.user.id)
		#news.save()
		mails = []
		for i in SystemUser.objects.all():
			mails.append(i.email)
		message = ('no reply', news.title, 'uuganaaaaaa@gmail.com', mails)
		send_mass_mail((message,))
		return super(ManagerNewsCreateView, self).form_valid(form)

class ManagerNewsUpdateView(ManagerLoginRequired, g.FormView):
	form_class = NewsForm
	template_name = 'manager/news/news_form.html'
	success_url = reverse_lazy('manager:manager_news')

class ManagerNewsCategoryCreateView(ManagerLoginRequired, g.FormView):
	form_class = NewsCategoryForm
	success_url = reverse_lazy('manager:manager_news')
	template_name = "manager/news/news_category_form.html"

	def form_valid(self, form):
		print "fasdfasdfasdf"
		return super(ManagerNewsCategoryCreateView, self).form_valid(self)

class ManagerNewsCategoryUpdateView(PopupUpdate, ManagerLoginRequired, g.FormView):
	form_class = NewsCategoryForm
	success_url = reverse_lazy('manager_news')
	template_name = "manager/news/news_category_form.html"










class ManagerLessonView(ManagerLoginRequired, g.TemplateView):

	template_name = 'manager/lesson/lesson_list.html'

class ManagerLessonCreateView(ManagerLoginRequired, g.FormView):
	form_class = LessonForm
	template_name = 'manager/lesson/lesson_form.html'
	success_url = reverse_lazy('manager_lesson')

class ManagerLessonUpdateView(ManagerLoginRequired, g.FormView):
	form_class = LessonForm
	success_url = reverse_lazy('manager_lesson')
	template_name = 'manager/lesson/lesson_form.html'

class ManagerLessonCategoryCreateView(PopupCreate, ManagerLoginRequired, g.FormView):
	form_class = LessonCategoryForm
	template_name = 'manager/lesson/lesson_category_form.html'
	success_url = reverse_lazy('manager_competition')

class ManagerLessonCategoryUpdateView(PopupUpdate, ManagerLoginRequired, g.FormView):
	form_class = LessonCategoryForm
	template_name = 'manager/lesson/lesson_category_form.html'
	success_url = reverse_lazy('manager_competition')






class ManagerResearchView(ManagerLoginRequired, g.TemplateView):
	template_name = 'manager/research/research_list.html'

class ManagerResearchCreateView(ManagerLoginRequired, g.FormView):
	form_class = ResearchForm
	template_name = 'manager/research/research_form.html'
	success_url = reverse_lazy('manager_research')
	
class ManagerResearchUpdateView(ManagerLoginRequired, g.FormView):
	form_class = ResearchForm
	success_url = reverse_lazy('manager_research')
	template_name = 'manager/research/research_form.html'

class ManagerResearchCategoryCreateView(PopupCreate, ManagerLoginRequired, g.FormView):
	form_class = ResearchCategoryForm
	template_name = 'manager/research/research_category_form.html'
	success_url = reverse_lazy('manager_competition')

class ManagerResearchCategoryUpdateView(PopupUpdate, ManagerLoginRequired, g.FormView):
	form_class = ResearchCategoryForm
	template_name = 'manager/research/research_category_form.html'
	success_url = reverse_lazy('manager_competition')
	






class ManagerUserListView(ManagerLoginRequired, g.TemplateView):
	template_name = 'manager/user/user.html'







class ManagerAdminUserListView(ManagerLoginRequired, g.TemplateView):
	template_name = 'manager/user/admin/admin_user_list.html'

class ManagerAdminUserCreateView(ManagerLoginRequired, g.FormView):
	form_class = ManagerForm
	template_name = 'manager/user/admin/admin_user_form.html'
	success_url = reverse_lazy('manager:manager_admin_user_list')

	def form_valid(self, form):
		user = form.save()
		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		text = 'http://127.0.0.1:8000/reset/%s/%s/' %(uid, token)
		send_mail('subject', text, 'uuganaaaaaa@gmail.com', [user.email])
		return super(ManagerAdminUserCreateView, self).form_valid(form)

class ManagerAdminUserUpdateView(ManagerLoginRequired, g.FormView):
	form_class = ManagerUpdateForm
	template_name = 'manager/user/admin/admin_user_form.html'
	success_url = reverse_lazy('manager:manager_admin_user_list')
	







class ManagerCompetitionRegisterView(ManagerLoginRequired, g.TemplateView):
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







class ManagerFinanceView(ManagerLoginRequired, g.TemplateView):
	get_perm = 'add_medee'
	template_name = 'manager/finance/finance.html'







class ManagerSupportMessageView(ManagerLoginRequired, g.FormView):

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