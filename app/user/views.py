# -*- coding:utf-8 -*-

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views import generic as g
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import SystemUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
#from django.template import RequestContext

__all__ = ['Home' ,'Login', 'RegisterView', 'register_confirm']

#def handler404(request):
#	response = render_to_response('user/base/base.html', {},
#                                  context_instance=RequestContext(request))
#	response.status_code = 404
#	return response

#def handler500(request):
#	response = render_to_response('user/base/base.html', {}, context_instance=RequestContext(request))
#	response.status_code = 500
#	return response

class Home(g.TemplateView):
	template_name = 'user/home/home.html'

class Login(g.FormView):
	form_class = LoginForm
	template_name = "user/login.html"
	success_url = reverse_lazy('web:home')

	def dispatch(self, request, *args, **kwargs):
		if SystemUser.objects.filter(id = request.user.id):
			return HttpResponseRedirect(reverse_lazy('web:home'))
		return super(Login, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
		if user and SystemUser.objects.filter(id = user.id):
			login(self.request, user)
			messages.success(self.request, u"Монексд тавтай морил %s" %user.username)
			url = self.request.GET.get('next', None)
			if url:
				return HttpResponseRedirect(url)
			return super(Login, self).form_valid(form)
		else:
			return super(Login, self).form_invalid(form)

	@staticmethod
	def logout(request):
		username = request.user.username
		logout(request)
		messages.warning(request, u"Дахин уулзахдаа баяртай байх болно %s." %username)
		return HttpResponseRedirect(reverse_lazy('web:home'))


class RegisterView(g.CreateView):
	form_class = RegisterForm
	template_name = "user/register.html"
	success_url = reverse_lazy('web:home')

	def form_valid(self, form):
		user = form.save()
		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		text = 'http://127.0.0.1:8000/reset/%s/%s/' %(uid, token)
		send_mail('subject', text, 'uuganaaaaaa@gmail.com', [user.email])
		messages.success(
			self.request,
			u"Бүртгэл амжилттай хийгдлээ. %s мэйл хаяг руу орж бүртгэлээ баталгаажуулна уу" %user.email
			)
		return super(RegisterView, self).form_valid(form)