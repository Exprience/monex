# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import json
import hashlib
import urllib
from datetime import datetime

from django.contrib.messages.views import SuccessMessageMixin
from django.template import Template, Context
from django.core.urlresolvers import reverse_lazy
from django.views import generic as g
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils.html import escape
from django.shortcuts import redirect
from django.contrib import messages


from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.utils.html import format_html
from django.utils.translation import ugettext as _


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator



import forms as manager_form
from app.competition.forms import *
from app.web import forms as web_form
from app.online_support.forms import SupportManagerMessageForm
from app.config import session
from managers import ManagerBaseDataManager as manager
from django.forms.utils import ErrorList
from django.contrib import messages


#Export
__all__ = []


class ManagerLoginView(g.FormView):
	form_class = manager_form.ManagerLoginForm
	template_name = 'manager/login.html'
	success_url = reverse_lazy('manager:manager_home')

	def get_success_url(self):
		return self.request.GET.get('next', self.success_url)

	def form_valid(self, form):
		user = manager.loginManager(form.cleaned_data['email'], form.cleaned_data['password'])
		session.put(self.request, 'manager', user)
		return super(ManagerLoginView, self).form_valid(form)

	@staticmethod
	def logout(request):
		session.pop(request, 'manager')
		return HttpResponseRedirect(reverse_lazy('manager:manager_login'))


class ManagerLoginRequired(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user is None:
			next_url = urllib.urlencode({'next': request.get_full_path()})
			return redirect('%s?%s' % (reverse_lazy('manager:manager_login'), next_url))
		return super(ManagerLoginRequired, self).dispatch(request, *args, **kwargs)


class ManagerHomeView(ManagerLoginRequired, g.TemplateView):
	
	template_name = 'manager/home.html'


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


class ManagerCompetitionRankCreateView(ManagerLoginRequired, g.FormView):
	form_class = CompetitionRankForm
	template_name = 'manager/competition/competition_rank_form.html'
	success_url = reverse_lazy('manager_competition')


class ManagerCompetitionRankUpdateView(ManagerLoginRequired, g.FormView):
	form_class = CompetitionRankForm
	template_name = 'manager/competition/competition_rank_form.html'
	success_url = reverse_lazy('manager_competition')


class ManagerCompetitionFilter(g.TemplateView):
	template_name = 'manager/competition/competition_filter.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ManagerCompetitionFilter, self).get_context_data(*args, **kwargs)
		return context


class NewsListView(ManagerLoginRequired, g.TemplateView):
	
	template_name = 'manager/news/news_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(NewsListView, self).get_context_data(*args, **kwargs)
		context['news'] = manager.show_lists(self.request.user.id, 'N')
		return context


class NewsCreateView(SuccessMessageMixin ,ManagerLoginRequired, g.FormView):
	form_class = manager_form.NewsForm
	template_name = 'manager/news/news_form.html'
	success_url = reverse_lazy('manager:news')
	success_message = u'Мэдээ амжилттай хадгадагдлаа'


	def get_form_kwargs(self):
		kwargs = super(NewsCreateView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'1'})
		return kwargs

	def form_valid(self, form):
		category = form.cleaned_data['category']
		title = form.cleaned_data['title']
		body = form.cleaned_data['body']
		manager.create('N', self.request.user.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), category, title = title, body = body)
		return super(NewsCreateView, self).form_valid(form)


class NewsUpdateView(SuccessMessageMixin, ManagerLoginRequired, g.FormView):
	form_class = manager_form.NewsForm
	template_name = 'manager/news/news_form.html'
	success_url = reverse_lazy('manager:news')
	success_message = u'Мэдээ амжилттай шинэчлэгдлээ.'

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(NewsUpdateView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(NewsUpdateView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'1', 'id':self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(NewsUpdateView, self).get_context_data(*args, **kwargs)
		context['object'] = True
		return context

	def form_valid(self, form):
		category = form.cleaned_data['category']
		title = form.cleaned_data['title']
		body = form.cleaned_data['body']
		result = manager.update('N', self.request.user.id, self.pk, category, title = title, body = body)
		if result:
			if not result.isSuccess:
				form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
				return self.form_invalid(form)
		else:
			form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
			return self.form_invalid(form)
		return super(NewsUpdateView, self).form_valid(form)


class NewsDeleteView(SuccessMessageMixin, ManagerLoginRequired, g.FormView):
	form_class = manager_form.NewsForm
	template_name = 'manager/news/news_delete.html'
	success_url = reverse_lazy('manager:news')
	success_message = u'Мэдээ амжилттай утслаа'

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(NewsDeleteView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(NewsDeleteView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'1', 'id':self.pk, 'is_delete':True})
		return kwargs

	def form_valid(self, form):
		manager.delete('N', self.request.user.id, self.pk)
		if result == False:
			form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
			return self.form_invalid(form)
		if result == None:
			form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
			return self.form_invalid(form)
		return super(NewsDeleteView, self).form_valid(form)


class NewsCategoryCreateUpdateView(ManagerLoginRequired, g.FormView):
	form_class = manager_form.CategoryForm
	success_url = reverse_lazy('manager:news')
	template_name = "manager/news/news_category_form.html"

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(NewsCategoryCreateUpdateView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(NewsCategoryCreateUpdateView, self).get_form_kwargs()
		kwargs.update({'id': self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(NewsCategoryCreateUpdateView, self).get_context_data(*args, **kwargs)
		context['object'] = self.pk
		return context

	def form_valid(self, form):		
		if "_popup" in self.request.POST:
			if not self.pk:
				result = manager.category_create(form.cleaned_data['category'], '', '1')
				if not result:
					form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
						return self.form_invalid(form)
				return HttpResponse('<script>opener.dismissAddRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(result.categoryId.value, form.cleaned_data['category']))
			else:
				result = manager.category_create(form.cleaned_data['category'], self.pk, '1', is_create = False)
				if not result:
					form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
						return self.form_invalid(form)
				return HttpResponse('<script>opener.dismissChangeRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(self.pk, form.cleaned_data['category']))


class NewsCategoryDeleteView(ManagerLoginRequired, g.FormView):

	template_name = 'manager/news/news_category_delete.html'
	form_class = manager_form.CategoryForm

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(NewsCategoryDeleteView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(NewsCategoryDeleteView, self).get_form_kwargs()
		kwargs.update({'delete_id' : self.pk})
		return kwargs


	def form_valid(self, form):
		result = manager.category_delete(self.request.user.id, self.pk, '1')
		if not result:
			form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
			return self.form_invalid(form)
		else:
			if result == '0':
				form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
				return self.form_invalid(form)
		return HttpResponse('<script>opener.dismissDeleteRelatedObjectPopup(window, "select", "%s");</script>' %self.pk)


class LessonListView(ManagerLoginRequired, g.TemplateView):
	template_name = 'manager/lesson/lesson_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(LessonListView, self).get_context_data(*args, **kwargs)
		context['lessons'] = manager.show_lists(self.request.user.id, 'L')
		return context


class LessonCreateView(SuccessMessageMixin, ManagerLoginRequired, g.FormView):
	form_class = manager_form.LessonForm
	template_name = 'manager/lesson/lesson_form.html'
	success_url = reverse_lazy('manager:lesson_list')
	success_message = u'Сургалт амжилттай хадгалагдлаа.'

	def get_form_kwargs(self):
		kwargs = super(LessonCreateView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'3'})
		return kwargs

	def form_valid(self, form):
		category = form.cleaned_data['category']
		title = form.cleaned_data['title']
		url = form.cleaned_data['url']
		author_name = form.cleaned_data['author_name']
		author_email = form.cleaned_data['author_email']
		manager.create('L', self.request.user.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), category, title = title, url = url, author_name = author_name, author_email = author_email)
		return super(LessonCreateView, self).form_valid(form)


class LessonUpdateView(SuccessMessageMixin, ManagerLoginRequired, g.FormView):
	form_class = manager_form.LessonForm
	success_url = reverse_lazy('manager:lesson_list')
	template_name = 'manager/lesson/lesson_form.html'
	success_message = u'Сургалт амжилттай шинэчлэгдлээ.'

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(LessonUpdateView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(LessonUpdateView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'3', 'id':self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(LessonUpdateView, self).get_context_data(*args, **kwargs)
		context['object'] = True
		return context

	def form_valid(self, form):
		category = form.cleaned_data['category']
		title = form.cleaned_data['title']
		url = form.cleaned_data['url']
		author_email = form.cleaned_data['author_email']
		author_name = form.cleaned_data['author_name']
		result = manager.update('L', self.request.user.id, self.pk, category, title = title, url = url, author_email = author_email, author_name = author_name)
		if result:
			if not result.isSuccess:
				form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
				return self.form_invalid(form)
		else:
			form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
			return self.form_invalid(form)
		return super(LessonUpdateView, self).form_valid(form)


class LessonDeleteView(SuccessMessageMixin, ManagerLoginRequired, g.FormView):
	form_class = manager_form.LessonForm
	success_url = reverse_lazy('manager:lesson_list')
	template_name = 'manager/lesson/lesson_delete.html'
	success_message = u'Сургалт амжилттай устлаа.'

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(LessonDeleteView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(LessonDeleteView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'3', 'id':self.pk, 'is_delete': True})
		return kwargs

	def form_valid(self, form):
		result = manager.delete('L', self.request.user.id, self.pk)
		if result == False:
			form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
			return self.form_invalid(form)
		if result == None:
			form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
			return self.form_invalid(form)
		return super(LessonDeleteView, self).form_valid(form)


class LessonCategoryCreateUpdateView(ManagerLoginRequired, g.FormView):
	form_class = manager_form.CategoryForm
	template_name = 'manager/lesson/lesson_category_form.html'
	success_url = reverse_lazy('manager:lesson_list')

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(LessonCategoryCreateUpdateView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(LessonCategoryCreateUpdateView, self).get_form_kwargs()
		kwargs.update({'id': self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(LessonCategoryCreateUpdateView, self).get_context_data(*args, **kwargs)
		context['object'] = self.pk
		return context

	def form_valid(self, form):		
		if "_popup" in self.request.POST:
			if not self.pk:
				result = manager.category_create(form.cleaned_data['category'], '', '3')
				if not result:
					form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
						return self.form_invalid(form)
				return HttpResponse('<script>opener.dismissAddRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(result.categoryId.value, form.cleaned_data['category']))
			else:
				result = manager.category_create(form.cleaned_data['category'], self.pk, '3', is_create = False)
				if not result:
					form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
						return self.form_invalid(form)
				return HttpResponse('<script>opener.dismissChangeRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(self.pk, form.cleaned_data['category']))


class LessonCategoryDeleteView(ManagerLoginRequired, g.FormView):

	template_name = 'manager/news/news_category_delete.html'
	form_class = manager_form.CategoryForm

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(LessonCategoryDeleteView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(LessonCategoryDeleteView, self).get_form_kwargs()
		kwargs.update({'delete_id' : self.pk})
		return kwargs


	def form_valid(self, form):
		result = manager.category_delete(self.request.user.id, self.pk, '3')
		if not result:
			form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
			return self.form_invalid(form)
		else:
			if result == '0':
				form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
				return self.form_invalid(form)
		return HttpResponse('<script>opener.dismissDeleteRelatedObjectPopup(window, "select", "%s");</script>' %self.pk)


class ManagerResearchView(ManagerLoginRequired, g.TemplateView):
	
	template_name = 'manager/research/research_list.html'


class ResearchCreateView(ManagerLoginRequired, g.FormView):
	form_class = manager_form.ResearchForm
	template_name = 'manager/research/research_form.html'
	success_url = reverse_lazy('manager_research')

	def get_form_kwargs(self):
		kwargs = super(ResearchCreateView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'2'})
		return kwargs

	
class ManagerResearchUpdateView(ManagerLoginRequired, g.FormView):
	form_class = manager_form.ResearchForm
	success_url = reverse_lazy('manager_research')
	template_name = 'manager/research/research_form.html'


class ManagerResearchCategoryCreateView(ManagerLoginRequired, g.FormView):
	form_class = web_form.ResearchCategoryForm
	template_name = 'manager/research/research_category_form.html'
	success_url = reverse_lazy('manager_competition')


class ManagerResearchCategoryUpdateView(ManagerLoginRequired, g.FormView):
	form_class = web_form.ResearchCategoryForm
	template_name = 'manager/research/research_category_form.html'
	success_url = reverse_lazy('manager_competition')
	

class ManagerUserListView(ManagerLoginRequired, g.TemplateView):
	
	template_name = 'manager/user/user.html'


class ManagerInfoView(ManagerLoginRequired, g.FormView):
	form_class = manager_form.ManagerForm
	template_name = 'manager/user/admin/admin_info.html'

	def get_form_kwargs(self):
		kwargs = super(ManagerInfoView, self).get_form_kwargs()
		kwargs.update({'info': True, 'id':self.request.user.id})
		return kwargs


class PasswordUpdateView(ManagerLoginRequired, g.FormView):
	form_class = manager_form.PasswordUpdateForm
	template_name = 'manager/user/admin/password_update.html'
	success_url = reverse_lazy('manager:manager_home')

	def form_valid(self, form):
		result = form.save(self.request)
		if not result:
			form._errors['__all__'] = ErrorList([u'Хуучин нууц үг буруу байна.'])
			return self.form_invalid(form)
		return super(PasswordUpdateView, self).form_valid(form)


class ManagerListView(ManagerLoginRequired, g.TemplateView):
	template_name = 'manager/user/admin/admin_user_list.html'

	def dispatch(self, request, *args, **kwargs):
		if request.user:
			if request.user.is_superuser == '0':
				raise Http404
		return super(ManagerListView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(ManagerListView, self).get_context_data(*args, **kwargs)
		context['managers'] = manager.manager_list()
		return context


class ManagerCreateUpdateView(SuccessMessageMixin, ManagerLoginRequired, g.FormView):
	form_class = manager_form.ManagerForm
	template_name = 'manager/user/admin/admin_user_form.html'
	success_url = reverse_lazy('manager:manager_list')
	success_message = u"Үйлдэл амжилттай хийгдлээ."

	def get_context_data(self, *args, **kwargs):
		context = super(ManagerCreateUpdateView, self).get_context_data(*args, **kwargs)
		if 'pk' in self.kwargs:
			context['object'] = self.kwargs['pk']
		return context

	def get_form_kwargs(self):
		kwargs = super(ManagerCreateUpdateView, self).get_form_kwargs()
		if 'pk' in self.kwargs:
			kwargs.update({'id': self.kwargs['pk']})
		return kwargs

	def form_valid(self, form):
		form.save(self.request)
		return super(ManagerCreateUpdateView, self).form_valid(form)
	

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


class ManagerSetPasswordView(g.FormView):
	form_class = manager_form.ManagerSetPasswordForm
	template_name = 'manager/password/set_password.html'
	success_url = reverse_lazy('manager:manager_login')

	def dispatch(self, request, *args , **kwargs):
		uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
		self.user = manager.check_manager(uid)
		if not default_token_generator.check_token(self.user, self.kwargs.pop('token', None)):
			raise Http404
		return super(ManagerSetPasswordView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.save(self.request, self.user)
		return super(ManagerSetPasswordView, self).form_valid(form)
