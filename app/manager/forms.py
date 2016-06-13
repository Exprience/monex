# -*- coding:utf-8 -*-

from django import forms
from app.user.forms import LoginForm
from django.contrib.auth import authenticate
from .models import Manager
from django.utils.translation import ugettext as _

class ManagerLoginForm(LoginForm):

	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		if self.is_valid():
			user = authenticate(username = cleaned_data['username'], password = cleaned_data['password'])
			if not user:
				raise forms.ValidationError(_(u'Хэрэглэгчийн нэр эсвэл нууц үг буруу байна'), code='invalid')
			else:
				if not Manager.objects.filter(username = user.username):
					raise forms.ValidationError(_(u'Хэрэглэгчийн нэр эсвэл нууц үг буруу байна'), code='invalid')
		return cleaned_data