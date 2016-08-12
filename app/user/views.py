# -*- coding:utf-8 -*-
import jsonpickle

from django.http import HttpResponseRedirect
from django.views import generic as g
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from .forms import RegisterForm,  LoginForm, UserPasswordResetForm, UserPasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django.contrib.auth.models import AbstractUser
import models as m
import forms as f
from managers import BaseDataManager as manager
from django.conf import settings

def put(request, name, value):
    request.session[name] = jsonpickle.encode(value)


__all__ = ['Home' ,'Login', 'RegisterView', 'ResetPasswordView']

class Home(g.TemplateView):
	template_name = 'user/base/home.html'



class Login(g.FormView):
	form_class = f.LoginForm
	template_name = "user/register/login.html"
	success_url = reverse_lazy('web:home')

	def dispatch(self, request, *args, **kwargs):
		if m.SystemUser.objects.filter(id = request.user.id):
			return HttpResponseRedirect(reverse_lazy('web:home'))
		return super(Login, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		user =  manager.loginUser(form.cleaned_data['username'], form.cleaned_data['password'])
		if user.isHavePrivilege:
			messages.success(self.request, u"Монексд тавтай морил")
			url = self.request.GET.get('next', None)
			put(self.request, 'user', user)
			print user.is_authenticated()
			if url:
				return HttpResponseRedirect(url)
			return super(Login, self).form_valid(form)
		else:
			return super(Login, self).form_invalid(form)

	@staticmethod
	def logout(request):
		username = request.user.username
		messages.warning(request, u"Дахин уулзахдаа баяртай байх болно %s." %username)
		return HttpResponseRedirect(reverse_lazy('web:home'))


class RegisterView(FormView):
	form_class = RegisterForm
	template_name = "user/register/register.html"
	success_url = reverse_lazy('register_confirm')

	def form_valid(self, form):
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
	#	username = form.cleaned_data['username']
	#	email = form.cleaned_data['email']
	#	password = form.cleaned_data['password']
	#	repeat_password = form.cleaned_data['repeat_password']
		
	#	user = form.save()
	#	uid = urlsafe_base64_encode(force_bytes1(user.pk))
	#	token = default_token_generator.make_token(user)
	#	text = 'http://127.0.0.1:8000/confirm/%s/%s/' %(uid, token)
	#	send_mail('subject', text, 'uuganaaaaaa@gmail.com', [user.email])
		context = {}
	#	context['email'] = user.email
	#	return render_to_response('user/register/register_confirm.html', context)
		return super(RegisterView, self).form_valid(form)
		
class ResetPasswordView(TemplateView):
	form_class = UserPasswordResetForm
	template_name = "user/password/password_reset.html"
	success_url = reverse_lazy('web:home')
#class UserSetPassView(TemplateView)
