# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import urllib


from django import http
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator


import forms as mf
from models import ResearchModel
from managers import ManagerDataManager as m
from app.config import session, status as s, views as v, config
from app.web.managers import WebDataManager as wm


class Login(v.FormView):
	form_class = mf.LoginForm
	success_url = reverse_lazy('manager:home')
	success_message = u"Монекд тавтай морил %(email)s"

	def get_success_url(self):
		return self.request.GET.get('next', self.success_url)

	def form_valid(self, form):
		user = m.login(form.cleaned_data['email'], form.cleaned_data['password'])
		
		if user == "false":
			return self.form_error(form, u"Хэрэглэгчийн и-мэйл эсвэл нууц үг буруу байна")
		
		if user.is_active == '0':
			return self.form_error(form, u"Системд нэвтрэх эрхгүй байна. Бүртгэлээ баталгаажуулна уу!")
		session.put(self.request, 'manager', user)
		return super(Login, self).form_valid(form)

	@staticmethod
	def logout(request):
		session.pop(request, 'manager')
		return http.HttpResponseRedirect(reverse_lazy('manager:manager_login'))


class LoginRequired(object):
	
	def dispatch(self, request, *args, **kwargs):
		if request.user is None:
			next_url = urllib.urlencode({'next': request.get_full_path()})
			return redirect('%s?%s' % (reverse_lazy('manager:manager_login'), next_url))
		if not hasattr(request.user, "is_manager"):
			raise http.Http404
		return super(LoginRequired, self).dispatch(request, *args, **kwargs)


class FormView(LoginRequired, v.FormView):
	pass


class TemplateView(LoginRequired, v.TemplateView):
	pass


class Home(TemplateView):
	pass


#Competitions
class CompetitionList(TemplateView):

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionList, self).get_context_data(*args, **kwargs)
		context['competitions'] = m.select(self.request.user.id, 'C')
		return context

class CompetitionCreate(FormView):
	form_class = mf.CompetitionForm
	success_url = reverse_lazy('manager:competition_list')
	success_message = u"Тэмцээн амжилттай шинэчлэгдлээ"

	def get_form_kwargs(self):
		kwargs = super(CompetitionCreate, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'4'})
		return kwargs

	def form_valid(self, form):
		category = form.cleaned_data['category']
		register_low = form.cleaned_data['register_low']
		prize = form.cleaned_data['prize']
		start_date = form.cleaned_data['start_date']
		end_date = form.cleaned_data['end_date']
		fee = form.cleaned_data['fee']
		m.create('C', self.request.user.id, category, status = s.COMPETITION_START_REGISTER, register_low = register_low, start_date = start_date, end_date = end_date, prize = prize, fee = fee)
		return super(CompetitionCreate, self).form_valid(form)

class CompetitionUpdate(FormView):
	form_class = mf.CompetitionForm
	success_url = reverse_lazy('manager:competition_list')
	success_message = u"Тэмцээн амжилттай шинэчлэгдлээ"

	def get_form_kwargs(self):
		kwargs = super(CompetitionUpdate, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'4', 'id':self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionUpdate, self).get_context_data(*args, **kwargs)
		context['object'] = True
		return context

	def form_valid(self, form):
		category = form.cleaned_data['category']
		register_low = form.cleaned_data['register_low']
		prize = form.cleaned_data['prize']
		start_date = form.cleaned_data['start_date']
		end_date = form.cleaned_data['end_date']
		fee = form.cleaned_data['fee']
		result = m.update('C', self.request.user.id, self.pk, category, register_low = register_low, start_date = start_date, end_date = end_date, prize = prize, fee = fee)
		if not result.isSuccess:
			self.error(u'Үйлдэл амжилтгүй боллоо')
			return self.form_invalid(form)
		return super(CompetitionUpdate, self).form_valid(form)

class CompetitionCategoryCreate(FormView):
	form_class = mf.CompetitionCategoryForm
	success_url = reverse_lazy('manager:competition_list')

	def get_form_kwargs(self):
		kwargs = super(CompetitionCategoryCreate, self).get_form_kwargs()
		kwargs.update({'id': self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionCategoryCreate, self).get_context_data(*args, **kwargs)
		context['object'] = self.pk
		return context

	def form_valid(self, form):		
		if "_popup" in self.request.POST:
			if not self.pk:
				result = m.category_create(form.cleaned_data['category'], '', '4', wallet_val = form.cleaned_data['wallet_val'])
				if not result:
					self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						self.error(u'Үйлдэл амжилтгүй боллоо')
						return self.form_invalid(form)
				return http.HttpResponse('<script>opener.dismissAddRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(result.categoryId.value, form.cleaned_data['category']))
			else:
				result = m.category_create(form.cleaned_data['category'], self.pk, '4', is_create = False, wallet_val = form.cleaned_data['wallet_val'])
				if not result:
					self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						self.error(u'Үйлдэл амжилтгүй боллоо')
						return self.form_invalid(form)
				return http.HttpResponse('<script>opener.dismissChangeRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(self.pk, form.cleaned_data['category']))

class CompetitionCategoryDelete(FormView):
	form_class = mf.CategoryForm

	def get_form_kwargs(self):
		kwargs = super(CompetitionCategoryDelete, self).get_form_kwargs()
		kwargs.update({'delete_id' : self.pk})
		return kwargs


	def form_valid(self, form):
		result = m.category_delete(self.request.user.id, self.pk, '4')
		if not result:
			self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
			return self.form_invalid(form)
		else:
			if result == '0':
				self.error(u'Үйлдэл амжилтгүй боллоо')
				return self.form_invalid(form)
		return http.HttpResponse('<script>opener.dismissDeleteRelatedObjectPopup(window, "select", "%s");</script>' %self.pk)

class CompetitionFilter(TemplateView):

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionFilter, self).get_context_data(*args, **kwargs)
		return context


#News
class NewsList(TemplateView):

	def get_context_data(self, *args, **kwargs):
		context = super(NewsList, self).get_context_data(*args, **kwargs)
		context['news'] = m.select(self.request.user.id, 'N')
		return context

class NewsCreate(FormView):
	form_class = mf.NewsForm
	success_url = reverse_lazy('manager:news')
	success_message = u'Мэдээ амжилттай хадгадагдлаа'


	def get_form_kwargs(self):
		kwargs = super(NewsCreate, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'1'})
		return kwargs

	def form_valid(self, form):
		category = form.cleaned_data['category']
		title = form.cleaned_data['title']
		body = form.cleaned_data['body']
		m.create('N', self.request.user.id, category, body = body, title = title)
		return super(NewsCreate, self).form_valid(form)

class NewsUpdate(FormView):
	form_class = mf.NewsForm
	success_url = reverse_lazy('manager:news')
	success_message = u'Мэдээ амжилттай шинэчлэгдлээ.'

	def get_form_kwargs(self):
		kwargs = super(NewsUpdate, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'1', 'id':self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(NewsUpdate, self).get_context_data(*args, **kwargs)
		context['object'] = True
		return context

	def form_valid(self, form):
		category = form.cleaned_data['category']
		title = form.cleaned_data['title']
		body = form.cleaned_data['body']
		result = m.update('N', self.request.user.id, self.pk, category, title = title, body = body)
		if result:
			if not result.isSuccess:
				self.error(u'Үйлдэл амжилтгүй боллоо')
				return self.form_invalid(form)
		else:
			self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
			return self.form_invalid(form)
		return super(NewsUpdate, self).form_valid(form)

class NewsDelete(FormView):
	form_class = mf.NewsForm
	success_url = reverse_lazy('manager:news')
	success_message = u'Мэдээ амжилттай утслаа'

	def get_form_kwargs(self):
		kwargs = super(NewsDelete, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'1', 'id':self.pk, 'is_delete':True})
		return kwargs

	def form_valid(self, form):
		result = m.delete('N', self.request.user.id, self.pk)
		if result == False:
			self.error(u'Үйлдэл амжилтгүй боллоо')
			return self.form_invalid(form)
		if result == None:
			self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
			return self.form_invalid(form)
		return super(NewsDelete, self).form_valid(form)

class NewsCategoryCreate(FormView):
	form_class = mf.CategoryForm
	success_url = reverse_lazy('manager:news')

	def get_form_kwargs(self):
		kwargs = super(NewsCategoryCreate, self).get_form_kwargs()
		kwargs.update({'id': self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(NewsCategoryCreate, self).get_context_data(*args, **kwargs)
		context['object'] = self.pk
		return context

	def form_valid(self, form):		
		if "_popup" in self.request.POST:
			if not self.pk:
				result = m.category_create(form.cleaned_data['category'], '', '1')
				if not result:
					self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						self.error(u'Үйлдэл амжилтгүй боллоо')
						return self.form_invalid(form)
				return http.HttpResponse('<script>opener.dismissAddRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(result.categoryId.value, form.cleaned_data['category']))
			else:
				result = m.category_create(form.cleaned_data['category'], self.pk, '1', is_create = False)
				if not result:
					self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						self.error(u'Үйлдэл амжилтгүй боллоо')
						return self.form_invalid(form)
				return http.HttpResponse('<script>opener.dismissChangeRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(self.pk, form.cleaned_data['category']))

class NewsCategoryDelete(FormView):
	form_class = mf.CategoryForm

	def get_form_kwargs(self):
		kwargs = super(NewsCategoryDelete, self).get_form_kwargs()
		kwargs.update({'delete_id' : self.pk})
		return kwargs


	def form_valid(self, form):
		result = m.category_delete(self.request.user.id, self.pk, '1')
		if not result:
			self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
			return self.form_invalid(form)
		else:
			if result == '0':
				self.error(u'Үйлдэл амжилтгүй боллоо')
				return self.form_invalid(form)
		return http.HttpResponse('<script>opener.dismissDeleteRelatedObjectPopup(window, "select", "%s");</script>' %self.pk)


#Lesson
class LessonList(TemplateView):

	def get_context_data(self, *args, **kwargs):
		context = super(LessonList, self).get_context_data(*args, **kwargs)
		context['lessons'] = m.select(self.request.user.id, 'L')
		return context

class LessonCreate(FormView):
	form_class = mf.LessonForm
	success_url = reverse_lazy('manager:lesson_list')
	success_message = u'Сургалт амжилттай хадгалагдлаа.'

	def get_form_kwargs(self):
		kwargs = super(LessonCreate, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'3'})
		return kwargs

	def form_valid(self, form):
		category = form.cleaned_data['category']
		title = form.cleaned_data['title']
		url = form.cleaned_data['url']
		author_name = form.cleaned_data['author_name']
		author_email = form.cleaned_data['author_email']
		m.create('L', self.request.user.id, category, title = title, url = url, author_name = author_name, author_email = author_email)
		return super(LessonCreate, self).form_valid(form)

class LessonUpdate(FormView):
	form_class = mf.LessonForm
	success_url = reverse_lazy('manager:lesson_list')
	success_message = u'Сургалт амжилттай шинэчлэгдлээ.'

	def get_form_kwargs(self):
		kwargs = super(LessonUpdate, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'3', 'id':self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(LessonUpdate, self).get_context_data(*args, **kwargs)
		context['object'] = True
		return context

	def form_valid(self, form):
		category = form.cleaned_data['category']
		title = form.cleaned_data['title']
		url = form.cleaned_data['url']
		author_email = form.cleaned_data['author_email']
		author_name = form.cleaned_data['author_name']
		result = m.update('L', self.request.user.id, self.pk, category, title = title, url = url, author_email = author_email, author_name = author_name)
		if result:
			if not result.isSuccess:
				self.error(u'Үйлдэл амжилтгүй боллоо')
				return self.form_invalid(form)
		else:
			self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
			return self.form_invalid(form)
		return super(LessonUpdate, self).form_valid(form)

class LessonDelete(FormView):
	form_class = mf.LessonForm
	success_url = reverse_lazy('manager:lesson_list')
	success_message = u'Сургалт амжилттай устлаа.'

	def get_form_kwargs(self):
		kwargs = super(LessonDelete, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'3', 'id':self.pk, 'is_delete': True})
		return kwargs

	def form_valid(self, form):
		result = m.delete('L', self.request.user.id, self.pk)
		if result == False:
			self.error(u'Үйлдэл амжилтгүй боллоо')
			return self.form_invalid(form)
		if result == None:
			self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
			return self.form_invalid(form)
		return super(LessonDelete, self).form_valid(form)

class LessonCategoryCreate(FormView):
	form_class = mf.CategoryForm
	success_url = reverse_lazy('manager:lesson_list')

	def get_form_kwargs(self):
		kwargs = super(LessonCategoryCreate, self).get_form_kwargs()
		kwargs.update({'id': self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(LessonCategoryCreate, self).get_context_data(*args, **kwargs)
		context['object'] = self.pk
		return context

	def form_valid(self, form):		
		if "_popup" in self.request.POST:
			if not self.pk:
				result = m.category_create(form.cleaned_data['category'], '', '3')
				if not result:
					self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						self.error(u'Үйлдэл амжилтгүй боллоо')
						return self.form_invalid(form)
				return http.HttpResponse('<script>opener.dismissAddRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(result.categoryId.value, form.cleaned_data['category']))
			else:
				result = m.category_create(form.cleaned_data['category'], self.pk, '3', is_create = False)
				if not result:
					self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						self.error(u'Үйлдэл амжилтгүй боллоо')
						return self.form_invalid(form)
				return http.HttpResponse('<script>opener.dismissChangeRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(self.pk, form.cleaned_data['category']))

class LessonCategoryDelete(FormView):
	form_class = mf.CategoryForm

	def get_form_kwargs(self):
		kwargs = super(LessonCategoryDelete, self).get_form_kwargs()
		kwargs.update({'delete_id' : self.pk})
		return kwargs


	def form_valid(self, form):
		result = m.category_delete(self.request.user.id, self.pk, '3')
		if not result:
			self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
			return self.form_invalid(form)
		else:
			if result == '0':
				self.error(u'Үйлдэл амжилтгүй боллоо')
				return self.form_invalid(form)
		return http.HttpResponse('<script>opener.dismissDeleteRelatedObjectPopup(window, "select", "%s");</script>' %self.pk)


#Research
class ResearchList(TemplateView):

	def get_context_data(self, *args, **kwargs):
		context = super(ResearchList, self).get_context_data(*args, **kwargs)
		context['researchs'] = m.select(self.request.user.id, 'R')
		return context

class ResearchCreate(FormView):
	form_class = mf.ResearchForm
	success_url = reverse_lazy('manager:research_list')

	def get_form_kwargs(self):
		kwargs = super(ResearchCreate, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'2'})
		return kwargs

	def form_valid(self, form):
		category = form.cleaned_data['category']
		title = form.cleaned_data['title']
		file = form.cleaned_data['file']
		research = ResearchModel.objects.create(file = file)
		author_name = form.cleaned_data['author_name']
		author_email = form.cleaned_data['author_email']
		result = m.create('R', self.request.user.id, category, title = title, author_name = author_name, file = research.file, author_email = author_email)
		if not result:
			self.error(u"Үйлдэл амжилтгүй боллоо.")
			return super(ResearchCreate, self).form_invalid(form)
		return super(ResearchCreate, self).form_valid(form)
	
class ResearchUpdate(FormView):
	form_class = mf.ResearchForm
	success_url = reverse_lazy('manager:research_list')

	def get_form_kwargs(self):
		kwargs = super(ResearchUpdate, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'type':'2', 'id': self.pk})
		return kwargs

	def form_valid(self, form):
		category = form.cleaned_data['category']
		title = form.cleaned_data['title']
		file = form.cleaned_data['file']
		author_email = form.cleaned_data['author_email']
		author_name = form.cleaned_data['author_name']
		result = m.update('R', self.request.user.id, self.pk, category, title = title, author_email = author_email, author_name = author_name, file = file)
		if result:
			if not result.isSuccess:
				self.error(u'Үйлдэл амжилтгүй боллоо')
				return self.form_invalid(form)
		else:
			self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
			return self.form_invalid(form)
		return super(ResearchUpdate, self).form_valid(form)

class ResearchCategoryCreate(FormView):
	form_class = mf.CategoryForm
	success_url = reverse_lazy('manager:research_list')

	def get_form_kwargs(self):
		kwargs = super(ResearchCategoryCreate, self).get_form_kwargs()
		kwargs.update({'id': self.pk})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(ResearchCategoryCreate, self).get_context_data(*args, **kwargs)
		context['object'] = self.pk
		return context

	def form_valid(self, form):		
		if "_popup" in self.request.POST:
			if not self.pk:
				result = m.category_create(form.cleaned_data['category'], '', '2')
				if not result:
					self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						self.error(u'Үйлдэл амжилтгүй боллоо')
						return self.form_invalid(form)
				return http.HttpResponse('<script>opener.dismissAddRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(result.categoryId.value, form.cleaned_data['category']))
			else:
				result = m.category_create(form.cleaned_data['category'], self.pk, '2', is_create = False)
				if not result:
					self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
					return self.form_invalid(form)
				else:
					if result.isSuccess == 'false':
						self.error(u'Үйлдэл амжилтгүй боллоо')
						return self.form_invalid(form)
				return http.HttpResponse('<script>opener.dismissChangeRelatedObjectPopup(window, "select", "%s", "%s");</script>'%(self.pk, form.cleaned_data['category']))

class ResearchCategoryDelete(FormView):
	form_class = mf.CategoryForm

	def get_form_kwargs(self):
		kwargs = super(ResearchCategoryDelete, self).get_form_kwargs()
		kwargs.update({'delete_id' : self.pk})
		return kwargs


	def form_valid(self, form):
		result = m.category_delete(self.request.user.id, self.pk, '2')
		if not result:
			self.error(u'Системд алдаа гарлаа та засагдтал түр хүлээнэ үү')
			return self.form_invalid(form)
		else:
			if result == '0':
				self.error(u'Үйлдэл амжилтгүй боллоо')
				return self.form_invalid(form)
		return http.HttpResponse('<script>opener.dismissDeleteRelatedObjectPopup(window, "select", "%s");</script>' %self.pk)


#Bank
class BankListView(TemplateView):
	template_name = 'manager/bank/bank_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BankListView, self).get_context_data(*args, **kwargs)
		context['banks'] = m.bank(self.request.user.id, 'S')
		return context

class BankCreateUpdateView(FormView):
	form_class = mf.BankForm
	template_name = 'manager/bank/bank_form.html'
	success_url = reverse_lazy('manager:bank_list')
	success_message = u'Банк амжилттай хадгалагдлаа.'

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
			m.bank(self.request.user.id, 'C', name = name, short_name = short_name, icon = icon, id = "")
		else:
			m.bank(self.request.user.id, 'U', name = name, short_name = short_name, icon = icon, id = self.pk)
		return super(BankCreateUpdateView, self).form_valid(form)

class BankDeleteView(FormView):
	form_class = mf.BankForm
	success_url = reverse_lazy('manager:bank_list')
	template_name = 'manager/bank/bank_delete.html'
	success_message = u'Банк амжилттай устлаа.'

	def get_form_kwargs(self):
		kwargs = super(BankDeleteView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'id':self.pk, 'is_delete': True})
		return kwargs

	def form_valid(self, form):
		m.bank(self.request.user.id, 'D', id = self.pk)
		return super(BankDeleteView, self).form_valid(form)


#Currency
class CurrencyListView(TemplateView):
	template_name = 'manager/currency/currency_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(CurrencyListView, self).get_context_data(*args, **kwargs)
		context['currencys'] = m.currency(self.request.user.id, 'S')
		return context

class CurrencyCreateUpdateView(FormView):
	form_class = mf.CurrencyForm
	template_name = 'manager/currency/currency_form.html'
	success_url = reverse_lazy('manager:currency_list')
	success_message = u'Банк амжилттай хадгалагдлаа.'

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
			m.currency(self.request.user.id, 'C', name = name, short_name = short_name, icon = icon, symbol = symbol, id = "")
		else:
			m.currency(self.request.user.id, 'U', name = name, short_name = short_name, icon = icon, symbol = symbol, id = self.pk)
		return super(CurrencyCreateUpdateView, self).form_valid(form)

class CurrencyDeleteView(FormView):
	form_class = mf.CurrencyForm
	success_url = reverse_lazy('manager:currency_list')
	template_name = 'manager/currency/currency_delete.html'
	success_message = u'Банк амжилттай устлаа.'

	def get_form_kwargs(self):
		kwargs = super(CurrencyDeleteView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'id':self.pk, 'is_delete': True})
		return kwargs

	def form_valid(self, form):
		m.currency(self.request.user.id, 'D', id = self.pk)
		return super(CurrencyDeleteView, self).form_valid(form)


#Currency Value
class CurrencyValueListView(TemplateView):
	template_name = 'manager/currency/currency_value_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(CurrencyValueListView, self).get_context_data(*args, **kwargs)
		context['currencys'] = m.list("S", config.PREVIOUS, config.NOW)
		return context

class CurrencyValueCreateView(FormView):
	form_class = mf.CurrencyValueForm
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
		result = m.currency_create(self.request.user.id, bank, currency, buy, sell)
		print result
		return super(CurrencyValueCreateView, self).form_valid(form)


#Stock
class StockListView(TemplateView):
	template_name = 'manager/stock/stock_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(StockListView, self).get_context_data(*args, **kwargs)
		context['stocks'] = m.stock(self.request.user.id, 'S')
		return context

class StockCreateUpdateView(FormView):
	form_class = mf.StockForm
	template_name = 'manager/stock/stock_form.html'
	success_url = reverse_lazy('manager:stock_list')
	success_message = u'Банк амжилттай хадгалагдлаа.'

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
			m.stock(self.request.user.id, 'C', name = name, symbol = symbol, id = "")
		else:
			m.stock(self.request.user.id, 'U', name = name, symbol = symbol, id = self.pk)
		return super(StockCreateUpdateView, self).form_valid(form)

class StockDeleteView(FormView):
	form_class = mf.StockForm
	success_url = reverse_lazy('manager:stock_list')
	template_name = 'manager/stock/stock_delete.html'
	success_message = u'Банк амжилттай устлаа.'

	def get_form_kwargs(self):
		kwargs = super(StockDeleteView, self).get_form_kwargs()
		kwargs.update({'manager_id': self.request.user.id, 'id':self.pk, 'is_delete': True})
		return kwargs

	def form_valid(self, form):
		m.stock(self.request.user.id, 'D', id = self.pk)
		return super(StockDeleteView, self).form_valid(form)


#Stock Value
class StockValueListView(TemplateView):
	template_name = 'manager/stock/stock_value_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(StockValueListView, self).get_context_data(*args, **kwargs)
		context['stocks'] = m.list("S", config.PREVIOUS, config.NOW, is_currency = False)
		return context

class StockValueCreateView(FormView):
	form_class = mf.StockValueForm
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
		m.stock_create(self.request.user.id, stock, open, buy, sell, high, low, last, close, config.NOW)
		return super(StockValueCreateView, self).form_valid(form)


#User
class UserList(TemplateView):
	pass

#Admin
class AdminInfo(FormView):
	form_class = mf.ManagerForm

	def get_form_kwargs(self):
		kwargs = super(AdminInfo, self).get_form_kwargs()
		kwargs.update({'info': True, 'id':self.request.user.id})
		return kwargs

class AdminPasswordUpdate(FormView):
	form_class = mf.PasswordUpdateForm
	success_url = reverse_lazy('manager:home')
	success_message = u'Нууц үг амжилттай шинэчлэгдлээ'

	def form_valid(self, form):
		result = form.save(self.request)
		if not result:
			self.error(u'Хуучин нууц үг буруу байна.')
			return self.form_invalid(form)
		return super(AdminPasswordUpdate, self).form_valid(form)

class AdminList(TemplateView):

	def dispatch(self, request, *args, **kwargs):
		if request.user:
			if request.user.is_superuser == '0':
				raise http.Http404
		return super(AdminList, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(AdminList, self).get_context_data(*args, **kwargs)
		context['managers'] = m.admins()
		return context

class AdminCreate(FormView):
	form_class = mf.ManagerForm
	success_url = reverse_lazy('manager:manager_list')
	success_message = u"%(email)s амжилттай хадгалагдлаа."
	
	def get_context_data(self, *args, **kwargs):
		context = super(AdminCreate, self).get_context_data(*args, **kwargs)
		context['object'] = self.pk
		return context

	def get_form_kwargs(self):
		kwargs = super(AdminCreate, self).get_form_kwargs()
		if self.pk:
			kwargs.update({'id': self.pk})
		return kwargs

	def form_valid(self, form):
		result = form.save(self.request)
		return super(AdminCreate, self).form_valid(form)

class AdminPasswordSet(v.FormView):
	form_class = mf.ManagerSetPasswordForm
	success_url = reverse_lazy('manager:manager_login')
	success_message = u'Бүртгэл амжилттай баталгаажлаа.'

	def dispatch(self, request, *args , **kwargs):
		uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
		self.user = m.get_manager(uid)
		if not default_token_generator.check_token(self.user, self.kwargs.pop('token', None)):
			raise http.Http404
		return super(AdminPasswordSet, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		result = form.save(self.user)
		return super(AdminPasswordSet, self).form_valid(form)

class AdminPasswordReset(v.FormView):
	form_class = mf.PasswordResetForm

#Competition Register	
class CompetitionRegister(TemplateView):

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionRegister, self).get_context_data(*args, **kwargs)
		context['competitions'] = m.select(self.request.user.id, 'C')
		return context

class CompetitionRegisterUser(TemplateView):

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionRegisterUser, self).get_context_data(*args, **kwargs)
		context['users'] = wm.register('S', competition_id = self.pk, is_manager = True, manager_id = self.request.user.id)
		context['pk'] = self.pk
		return context

def approve(request, ck = 0, pk = 0):
	result = wm.register('U', id = pk, is_manager = True, manager_id = request.user.id, is_approved = True)
	messages.success(request, u'Үйлдэл амжилттай хийгдлээ')
	return http.HttpResponseRedirect(reverse_lazy('manager:competition_register_user_list' , kwargs = {'pk': ck}))

def decline(request, ck = 0, pk = 0):
	result = wm.register('U', id = pk, is_manager = True, manager_id = request.user.id)
	messages.success(request, u'Үйлдэл амжилттай хийгдлээ')
	return http.HttpResponseRedirect(reverse_lazy('manager:competition_register_user_list' , kwargs = {'pk': ck}))


#Finance
class ManagerFinanceView(TemplateView):
	get_perm = 'add_medee'
	template_name = 'manager/finance/finance.html'
