# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import urllib

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.conf import settings


from app.config import session, config, views as cv
from managers import UserDataManager as um
import forms as f 


class FormView(cv.FormView):
	pass

class TemplateView(cv.TemplateView):
	pass
		


class LoginRequired(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user is None:
			next_url = urllib.urlencode({'next': request.get_full_path()})
			return redirect('%s?%s' % (settings.LOGIN_URL, next_url))
		return super(LoginRequired, self).dispatch(request, *args, **kwargs)


class Home(TemplateView):

	template_name = 'user/base/home.html'

	def dispatch(self, request, *args, **kwargs):
		if hasattr(request.user, "is_manager"):
			return HttpResponseRedirect(reverse_lazy('manager:home'))
		return super(Home, self).dispatch(request, *args, **kwargs)


class Login(FormView):

	form_class = f.LoginForm
	success_url = reverse_lazy('web:home')
	success_message = u"Монекд тавтай морил"

	def get_success_url(self):
		return self.request.GET.get('next', self.success_url)

	def form_valid(self, form):
		user =  um.login(form.cleaned_data['username'], form.cleaned_data['password'])
		if user is None:
			self.form_error(form, u"Хэрэглэгчийн нэр эсвэл нууц үг буруу байна")
			return super(Login, self).form_invalid(form)
		else:
			session.put(self.request, 'user', user)
		return super(Login, self).form_valid(form)

	@staticmethod
	def logout(request):
		session.pop(request, 'user')
		return HttpResponseRedirect(reverse_lazy('web:home'))


class Register(FormView):
	form_class = f.RegisterForm
	template_name = "user/register/register.html"
	success_url = reverse_lazy('web:home')

	def form_valid(self, form):
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = um.register(username, email, password)
		if user.isSuccess:
			return super(Register, self).form_valid(form)
		else:
			self.error("Бүртгүүлэхэд алдаа гарлаа")
			return super(Register, self).form_invalid(form)
		

class ResetPassword(FormView):
	form_class = f.PasswordResetForm
	template_name = "user/password/password_reset.html"
	success_url = reverse_lazy('web:home')


class SetPassword(FormView):
	
	form_class = f.SetPasswordForm

	def password_change(request, template_name="user/password/password_reset_confirm.html", post_change_redirect=None):
		if post_change_redirect is None:
			post_change_redirect = reverse_lazy('web:home')
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(post_change_redirect)


class ChangePassword(LoginRequired, FormView):
	form_class = f.PasswordChangeForm
	template_name = "user/password/password_change.html"
	success_url  = reverse_lazy('web:home')





