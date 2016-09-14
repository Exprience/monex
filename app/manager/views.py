# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import urllib
from datetime import datetime
from dateutil.relativedelta import relativedelta


from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.views import generic as g
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import redirect
from django.forms.utils import ErrorList
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from app.online_support.forms import SupportManagerMessageForm


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator


import forms as manager_form
from app.web import forms as web_form
from app.config import session, status as s
from managers import ManagerBaseDataManager as manager



#Exports
__all__ = []

NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
PREVIOUS = (datetime.now() - relativedelta(month=1)).strftime("%Y-%m-%d %H:%M:%S")



class LoginView(g.FormView):
	form_class = manager_form.ManagerLoginForm
	template_name = 'manager/login.html'
	success_url = reverse_lazy('manager:manager_home')

	def get_success_url(self):
		return self.request.GET.get('next', self.success_url)

	def form_valid(self, form):
		user = manager.loginManager(form.cleaned_data['email'], form.cleaned_data['password'])
		session.put(self.request, 'manager', user)
		return super(LoginView, self).form_valid(form)

	@staticmethod
	def logout(request):
		session.pop(request, 'manager')
		return HttpResponseRedirect(reverse_lazy('manager:manager_login'))


class LoginRequired(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user is None:
			next_url = urllib.urlencode({'next': request.get_full_path()})
			return redirect('%s?%s' % (reverse_lazy('manager:manager_login'), next_url))
		return super(LoginRequired, self).dispatch(request, *args, **kwargs)


class HomeView(LoginRequired, g.TemplateView):
	
	template_name = 'manager/home.html'


class CompetitionListView(LoginRequired, g.TemplateView):
	template_name = 'manager/competition/competition_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionListView, self).get_context_data(*args, **kwargs)
		context['competitions'] = manager.select(self.request.user.id, 'C')
		return context

class CompetitionCreateView(SuccessMessageMixin, LoginRequired, g.FormView):
	form_class = manager_form.CompetitionForm
	template_name = 'manager/competition/competition_form.html'
	success_url = reverse_lazy('manager:competition_list')
	success_message = u"Тэмцээн амжилттай шинэчлэгдлээ"

	def get_form_kwargs(self):
		kwargs = super(CompetitionCreateView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'4'})
		return kwargs

	def form_valid(self, form):
		category = form.cleaned_data['category']
		register_low = form.cleaned_data['register_low']
		prize = form.cleaned_data['prize']
		start_date = form.cleaned_data['start_date']
		end_date = form.cleaned_data['end_date']
		fee = form.cleaned_data['fee']
		manager.create('C', self.request.user.id, NOW, category, status = s.COMPETITION_START_REGISTER, register_low = register_low, start_date = start_date, end_date = end_date, prize = prize, fee = fee)
		return super(CompetitionCreateView, self).form_valid(form)

class CompetitionUpdateView(SuccessMessageMixin, LoginRequired, g.FormView):
	form_class = manager_form.CompetitionForm
	template_name = 'manager/competition/competition_form.html'
	success_url = reverse_lazy('manager:competition_list')
	success_message = u"Тэмцээн амжилттай шинэчлэгдлээ"

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(CompetitionUpdateView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CompetitionUpdateView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'4', 'id':self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionUpdateView, self).get_context_data(*args, **kwargs)
		context['object'] = True
		return context

	def form_valid(self, form):
		category = form.cleaned_data['category']
		register_low = form.cleaned_data['register_low']
		prize = form.cleaned_data['prize']
		start_date = form.cleaned_data['start_date']
		end_date = form.cleaned_data['end_date']
		print type(end_date.strftime("%Y-%m-%d %H:%M:%S"))
		fee = form.cleaned_data['fee']
		result = manager.update('C', self.request.user.id, self.pk, category, register_low = register_low, start_date = start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date = end_date.strftime("%Y-%m-%d %H:%M:%S"), prize = prize, fee = fee)
		if result:
			if not result.isSuccess:
				form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
				return self.form_invalid(form)
		else:
			form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
			return self.form_invalid(form)
		return super(CompetitionUpdateView, self).form_valid(form)

class CompetitionCategoryCreateUpdateView(LoginRequired, g.FormView):
	form_class = manager_form.CompetitionCategoryForm
	template_name = 'manager/competition/competition_category_form.html'
	success_url = reverse_lazy('manager:competition_list')

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(CompetitionCategoryCreateUpdateView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CompetitionCategoryCreateUpdateView, self).get_form_kwargs()
		kwargs.update({'id': self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionCategoryCreateUpdateView, self).get_context_data(*args, **kwargs)
		context['object'] = self.pk
		return context

	def form_valid(self, form):		
		if "_popup" in self.request.POST:
			if not self.pk:
				result = manager.category_create(form.cleaned_data['category'], '', '4', wallet_val = form.cleaned_data['wallet_val'])
				if not result:
					form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
						return self.form_invalid(form)
				return HttpResponse('<script>opener.dismissAddRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(result.categoryId.value, form.cleaned_data['category']))
			else:
				result = manager.category_create(form.cleaned_data['category'], self.pk, '4', is_create = False)
				if not result:
					form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
						return self.form_invalid(form)
				return HttpResponse('<script>opener.dismissChangeRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(self.pk, form.cleaned_data['category']))

class CompetitionCategoryDeleteView(LoginRequired, g.FormView):

	template_name = 'manager/competition/competition_category_delete.html'
	form_class = manager_form.CategoryForm

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(CompetitionCategoryDeleteView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CompetitionCategoryDeleteView, self).get_form_kwargs()
		kwargs.update({'delete_id' : self.pk})
		return kwargs


	def form_valid(self, form):
		result = manager.category_delete(self.request.user.id, self.pk, '4')
		if not result:
			form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
			return self.form_invalid(form)
		else:
			if result == '0':
				form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
				return self.form_invalid(form)
		return HttpResponse('<script>opener.dismissDeleteRelatedObjectPopup(window, "select", "%s");</script>' %self.pk)

class CompetitionFilter(g.TemplateView):
	template_name = 'manager/competition/competition_filter.html'

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionFilter, self).get_context_data(*args, **kwargs)
		return context


class NewsListView(LoginRequired, g.TemplateView):
	
	template_name = 'manager/news/news_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(NewsListView, self).get_context_data(*args, **kwargs)
		context['news'] = manager.select(self.request.user.id, 'N')
		return context

class NewsCreateView(SuccessMessageMixin ,LoginRequired, g.FormView):
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
		manager.create('N', self.request.user.id, NOW, category, title = title, body = body)
		return super(NewsCreateView, self).form_valid(form)

class NewsUpdateView(SuccessMessageMixin, LoginRequired, g.FormView):
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

class NewsDeleteView(SuccessMessageMixin, LoginRequired, g.FormView):
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
		result = manager.delete('N', self.request.user.id, self.pk)
		if result == False:
			form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
			return self.form_invalid(form)
		if result == None:
			form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
			return self.form_invalid(form)
		return super(NewsDeleteView, self).form_valid(form)

class NewsCategoryCreateUpdateView(LoginRequired, g.FormView):
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

class NewsCategoryDeleteView(LoginRequired, g.FormView):

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


class LessonListView(LoginRequired, g.TemplateView):
	template_name = 'manager/lesson/lesson_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(LessonListView, self).get_context_data(*args, **kwargs)
		context['lessons'] = manager.select(self.request.user.id, 'L')
		return context

class LessonCreateView(SuccessMessageMixin, LoginRequired, g.FormView):
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
		manager.create('L', self.request.user.id, NOW, category, title = title, url = url, author_name = author_name, author_email = author_email)
		return super(LessonCreateView, self).form_valid(form)

class LessonUpdateView(SuccessMessageMixin, LoginRequired, g.FormView):
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

class LessonDeleteView(SuccessMessageMixin, LoginRequired, g.FormView):
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

class LessonCategoryCreateUpdateView(LoginRequired, g.FormView):
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

class LessonCategoryDeleteView(LoginRequired, g.FormView):

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


class ResearchListView(LoginRequired, g.TemplateView):
	
	template_name = 'manager/research/research_list.html'

class ResearchCreateView(LoginRequired, g.FormView):
	form_class = manager_form.ResearchForm
	template_name = 'manager/research/research_form.html'
	success_url = reverse_lazy('manager:research_list')

	def get_form_kwargs(self):
		kwargs = super(ResearchCreateView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'2'})
		return kwargs
	
class ResearchUpdateView(LoginRequired, g.FormView):
	form_class = manager_form.ResearchForm
	success_url = reverse_lazy('manager:research_list')
	template_name = 'manager/research/research_form.html'

class ResearchCategoryCreateUpdateView(LoginRequired, g.FormView):
	form_class = manager_form.CategoryForm
	template_name = 'manager/research/research_category_form.html'
	success_url = reverse_lazy('manager:research_list')

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(ResearchCategoryCreateUpdateView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(ResearchCategoryCreateUpdateView, self).get_form_kwargs()
		kwargs.update({'id': self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(ResearchCategoryCreateUpdateView, self).get_context_data(*args, **kwargs)
		context['object'] = self.pk
		return context

	def form_valid(self, form):		
		if "_popup" in self.request.POST:
			if not self.pk:
				result = manager.category_create(form.cleaned_data['category'], '', '2')
				if not result:
					form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
						return self.form_invalid(form)
				return HttpResponse('<script>opener.dismissAddRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(result.categoryId.value, form.cleaned_data['category']))
			else:
				result = manager.category_create(form.cleaned_data['category'], self.pk, '2', is_create = False)
				if not result:
					form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
						return self.form_invalid(form)
				return HttpResponse('<script>opener.dismissChangeRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(self.pk, form.cleaned_data['category']))

class ResearchCategoryDeleteView(LoginRequired, g.FormView):

	template_name = 'manager/news/news_category_delete.html'
	form_class = manager_form.CategoryForm

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(ResearchCategoryDeleteView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(ResearchCategoryDeleteView, self).get_form_kwargs()
		kwargs.update({'delete_id' : self.pk})
		return kwargs


	def form_valid(self, form):
		result = manager.category_delete(self.request.user.id, self.pk, '2')
		if not result:
			form._errors['__all__'] = ErrorList([u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү'])
			return self.form_invalid(form)
		else:
			if result == '0':
				form._errors['__all__'] = ErrorList([u'Үйлдэл амжилтгүй боллоо'])
				return self.form_invalid(form)
		return HttpResponse('<script>opener.dismissDeleteRelatedObjectPopup(window, "select", "%s");</script>' %self.pk)


class BankListView(LoginRequired, g.TemplateView):
	template_name = 'manager/bank/bank_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BankListView, self).get_context_data(*args, **kwargs)
		context['banks'] = manager.bank(self.request.user.id, 'S')
		return context

class BankCreateUpdateView(SuccessMessageMixin, LoginRequired, g.FormView):
	form_class = manager_form.BankForm
	template_name = 'manager/bank/bank_form.html'
	success_url = reverse_lazy('manager:bank_list')
	success_message = u'Банк амжилттай хадгалагдлаа.'

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(BankCreateUpdateView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(BankCreateUpdateView, self).get_form_kwargs()
		kwargs.update({'manager_id':self.request.user.id, 'id': self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(BankCreateUpdateView, self).get_context_data(*args, **kwargs)
		if self.pk:
			context['object'] = True
		return context

	def form_valid(self, form):
		name = form.cleaned_data['name']
		short_name = form.cleaned_data['short_name']
		icon = form.cleaned_data['icon']
		if not self.pk:
			manager.bank(self.request.user.id, 'C', name = name, short_name = short_name, icon = icon, id = "")
		else:
			manager.bank(self.request.user.id, 'U', name = name, short_name = short_name, icon = icon, id = self.pk)
		return super(BankCreateUpdateView, self).form_valid(form)

class BankDeleteView(SuccessMessageMixin, LoginRequired, g.FormView):
	form_class = manager_form.BankForm
	success_url = reverse_lazy('manager:bank_list')
	template_name = 'manager/bank/bank_delete.html'
	success_message = u'Банк амжилттай устлаа.'

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(BankDeleteView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(BankDeleteView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'id':self.pk, 'is_delete': True})
		return kwargs

	def form_valid(self, form):
		manager.bank(self.request.user.id, 'D', id = self.pk)
		return super(BankDeleteView, self).form_valid(form)


class CurrencyListView(LoginRequired, g.TemplateView):
	template_name = 'manager/currency/currency_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(CurrencyListView, self).get_context_data(*args, **kwargs)
		context['currencys'] = manager.currency(self.request.user.id, 'S')
		return context

class CurrencyCreateUpdateView(SuccessMessageMixin, LoginRequired, g.FormView):
	form_class = manager_form.CurrencyForm
	template_name = 'manager/currency/currency_form.html'
	success_url = reverse_lazy('manager:currency_list')
	success_message = u'Банк амжилттай хадгалагдлаа.'

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(CurrencyCreateUpdateView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CurrencyCreateUpdateView, self).get_form_kwargs()
		kwargs.update({'manager_id':self.request.user.id, 'id': self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(CurrencyCreateUpdateView, self).get_context_data(*args, **kwargs)
		if self.pk:
			context['object'] = True
		return context

	def form_valid(self, form):
		name = form.cleaned_data['name']
		short_name = form.cleaned_data['short_name']
		symbol = form.cleaned_data['symbol']
		icon = form.cleaned_data['icon']
		if not self.pk:
			manager.currency(self.request.user.id, 'C', name = name, short_name = short_name, icon = icon, symbol = symbol, id = "")
		else:
			manager.currency(self.request.user.id, 'U', name = name, short_name = short_name, icon = icon, symbol = symbol, id = self.pk)
		return super(CurrencyCreateUpdateView, self).form_valid(form)

class CurrencyDeleteView(SuccessMessageMixin, LoginRequired, g.FormView):
	form_class = manager_form.CurrencyForm
	success_url = reverse_lazy('manager:currency_list')
	template_name = 'manager/currency/currency_delete.html'
	success_message = u'Банк амжилттай устлаа.'

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(CurrencyDeleteView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CurrencyDeleteView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'id':self.pk, 'is_delete': True})
		return kwargs

	def form_valid(self, form):
		manager.currency(self.request.user.id, 'D', id = self.pk)
		return super(CurrencyDeleteView, self).form_valid(form)


class StockListView(LoginRequired, g.TemplateView):
	template_name = 'manager/stock/stock_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(StockListView, self).get_context_data(*args, **kwargs)
		context['stocks'] = manager.stock(self.request.user.id, 'S')
		return context

class StockCreateUpdateView(SuccessMessageMixin, LoginRequired, g.FormView):
	form_class = manager_form.StockForm
	template_name = 'manager/stock/stock_form.html'
	success_url = reverse_lazy('manager:stock_list')
	success_message = u'Банк амжилттай хадгалагдлаа.'

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(StockCreateUpdateView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(StockCreateUpdateView, self).get_form_kwargs()
		kwargs.update({'manager_id':self.request.user.id, 'id': self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(StockCreateUpdateView, self).get_context_data(*args, **kwargs)
		if self.pk:
			context['object'] = True
		return context

	def form_valid(self, form):
		name = form.cleaned_data['name']
		symbol = form.cleaned_data['symbol']
		if not self.pk:
			manager.stock(self.request.user.id, 'C', name = name, symbol = symbol, id = "")
		else:
			manager.stock(self.request.user.id, 'U', name = name, symbol = symbol, id = self.pk)
		return super(StockCreateUpdateView, self).form_valid(form)

class StockDeleteView(SuccessMessageMixin, LoginRequired, g.FormView):
	form_class = manager_form.StockForm
	success_url = reverse_lazy('manager:stock_list')
	template_name = 'manager/stock/stock_delete.html'
	success_message = u'Банк амжилттай устлаа.'

	def dispatch(self, request, *args, **kwargs):
		self.pk = self.kwargs.pop('pk', None)
		return super(StockDeleteView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(StockDeleteView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'id':self.pk, 'is_delete': True})
		return kwargs

	def form_valid(self, form):
		manager.stock(self.request.user.id, 'D', id = self.pk)
		return super(StockDeleteView, self).form_valid(form)


class CurrencyValueListView(LoginRequired, g.TemplateView):
	template_name = 'manager/currency/currency_value_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(CurrencyValueListView, self).get_context_data(*args, **kwargs)
		context['currencys'] = manager.list("S", PREVIOUS, NOW)
		return context

class CurrencyValueCreateView(SuccessMessageMixin, LoginRequired, g.FormView):
	form_class = manager_form.CurrencyValueForm
	template_name = 'manager/currency/currency_value_form.html'
	success_url = reverse_lazy('manager:currency_value_list')
	success_message = u'Валютын ханш амжилттай хадгалагдлаа'

	def get_form_kwargs(self):
		kwargs = super(CurrencyValueCreateView, self).get_form_kwargs()
		kwargs.update({'manager_id':self.request.user.id})
		return kwargs

	def form_valid(self, form):
		bank = form.cleaned_data['bank']
		currency = form.cleaned_data['currency']
		buy = form.cleaned_data['buy']
		sell = form.cleaned_data['sell']
		manager.currency_create(self.request.user.id, bank, currency, buy, sell)
		return super(CurrencyValueCreateView, self).form_valid(form)


class StockValueListView(LoginRequired, g.TemplateView):
	template_name = 'manager/stock/stock_value_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(StockValueListView, self).get_context_data(*args, **kwargs)
		context['stocks'] = manager.list("S", PREVIOUS, NOW, is_currency = False)
		return context

class StockValueCreateView(SuccessMessageMixin, LoginRequired, g.FormView):
	form_class = manager_form.StockValueForm
	template_name = 'manager/stock/stock_value_form.html'
	success_url = reverse_lazy('manager:stock_value_list')
	success_message = u'Хувьцааны ханш амжилттай хадгалагдлаа'

	def get_form_kwargs(self):
		kwargs = super(StockValueCreateView, self).get_form_kwargs()
		kwargs.update({'manager_id':self.request.user.id})
		return kwargs

	def form_valid(self, form):
		stock = form.cleaned_data['stock']
		open = form.cleaned_data['open']
		buy = form.cleaned_data['buy']
		sell = form.cleaned_data['sell']
		high = form.cleaned_data['high']
		low = form.cleaned_data['low']
		last = form.cleaned_data['last']
		close = form.cleaned_data['close']
		manager.stock_create(self.request.user.id, stock, open, buy, sell, high, low, last, close, NOW)
		return super(StockValueCreateView, self).form_valid(form)


class ManagerUserListView(LoginRequired, g.TemplateView):
	
	template_name = 'manager/user/user.html'

class ManagerInfoView(LoginRequired, g.FormView):
	form_class = manager_form.ManagerForm
	template_name = 'manager/user/admin/admin_info.html'

	def get_form_kwargs(self):
		kwargs = super(ManagerInfoView, self).get_form_kwargs()
		kwargs.update({'info': True, 'id':self.request.user.id})
		return kwargs

class PasswordUpdateView(LoginRequired, g.FormView):
	form_class = manager_form.PasswordUpdateForm
	template_name = 'manager/user/admin/password_update.html'
	success_url = reverse_lazy('manager:manager_home')

	def form_valid(self, form):
		result = form.save(self.request)
		if not result:
			form._errors['__all__'] = ErrorList([u'Хуучин нууц үг буруу байна.'])
			return self.form_invalid(form)
		return super(PasswordUpdateView, self).form_valid(form)

class ManagerListView(LoginRequired, g.TemplateView):
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

class ManagerCreateUpdateView(SuccessMessageMixin, LoginRequired, g.FormView):
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
	
class ManagerCompetitionRegisterView(LoginRequired, g.TemplateView):
	
	template_name = 'manager/competition/competition_register.html'


def manager_competition_register_view(request, id = 0):
	competition_register = CompetitionRegister.objects.get(id = id)
	competition_register.status = True
	competition_register.save()
	from notifications.signals import notify
	notify.send(request.user, recipient=request.user, verb='you reached level 10')
	return HttpResponseRedirect(reverse_lazy('manager:manager_competition_register'))


class ManagerFinanceView(LoginRequired, g.TemplateView):
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
