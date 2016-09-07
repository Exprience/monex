# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import urllib


from django.http import HttpResponseRedirect
from django.views import generic as g
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.conf import settings


from app.config import session
from managers import UserBaseDataManager as manager
from forms import UserRegisterForm,  UserLoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm


class UserLoginRequired(object):


	def dispatch(self, request, *args, **kwargs):
		if request.user is None:
			next_url = urllib.urlencode({'next': request.get_full_path()})
			return redirect('%s?%s' % (settings.LOGIN_URL, next_url))
		return super(UserLoginRequired, self).dispatch(request, *args, **kwargs)


class UserHome(g.TemplateView):

	template_name = 'user/base/home.html'


class UserLogin(g.FormView):

	form_class = UserLoginForm
	template_name = "user/register/login.html"
	success_url = reverse_lazy('web:home')

	def get_success_url(self):
		return self.request.GET.get('next', self.success_url)

	def form_valid(self, form):
		user =  manager.loginUser(form.cleaned_data['username'], form.cleaned_data['password'])
		if user.isHavePrivilege:
			messages.success(self.request, u"Монексд тавтай морил")
			session.put(self.request, 'user', user)
		return super(UserLogin, self).form_valid(form)

	@staticmethod
	def logout(request):
		session.pop(request, 'user')
		messages.warning(request, u"Дахин уулзахдаа баяртай байх болно.")
		return HttpResponseRedirect(reverse_lazy('web:home'))


class UserRegisterView(g.FormView):
	form_class = UserRegisterForm
	template_name = "user/register/register.html"
	success_url = reverse_lazy('web:home')

	def form_valid(self, form):
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = manager.register(username, email, password)
		if user:
			if user.isSuccess:
				return super(UserRegisterView, self).form_valid(form)
			else:
				return super(UserRegisterView, self).form_invalid(form)
		else:
			return super(UserRegisterView, self).form_invalid(form)

class UserResetPasswordView(g.FormView):
	form_class = UserPasswordResetForm
	template_name = "user/password/password_reset.html"
	post_change_redirect = reverse_lazy('web:home')


class UserSetPassView(g.FormView):
	
	form_class = UserSetPasswordForm

	def password_change(request, template_name="user/password/password_reset_confirm.html", post_change_redirect=None):
		if post_change_redirect is None:
			post_change_redirect = reverse_lazy('web:home')
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(post_change_redirect)


class UserChangePasswordView(UserLoginRequired, g.FormView):
	form_class = UserPasswordChangeForm
	template_name = "user/password/password_change.html"
	post_change_redirect  = reverse_lazy('web:home')





