# -*- coding:utf-8 -*-

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import FormView, TemplateView, UpdateView, CreateView
#from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import SystemUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
__all__ = ['Login', 'RegisterView', 'register_confirm']


#class SuccessMessage(SuccessMessageMixin):
#	success_message = 'Таны мэдээлэл амжилттай хадгалагдлаа'

class Login(FormView):
	form_class = LoginForm
	template_name = "user/login.html"
	success_url = reverse_lazy('home')

	def dispatch(self, request, *args, **kwargs):
		if SystemUser.objects.filter(username = request.user.username):
			return HttpResponseRedirect(reverse_lazy('home'))
		return super(Login, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
		if user and SystemUser.objects.filter(username = user.username):
			login(self.request, user)
			return super(Login, self).form_valid(form)
		else:
			return super(Login, self).form_invalid(form)

	@staticmethod
	def logout(request):
		logout(request)
		return HttpResponseRedirect(reverse_lazy('home'))



class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = "user/register.html"
	success_url = reverse_lazy('register_confirm')

	def form_valid(self, form):
		user = form.save()
		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		text = 'http://127.0.0.1:8000/confirm/%s/%s/' %(uid, token)
		send_mail('subject', text, 'uuganaaaaaa@gmail.com', [user.email])
		context = {}
		context['email'] = user.email
		return render_to_response('user/register_confirm.html', context)