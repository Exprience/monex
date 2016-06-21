# -*- coding:utf-8 -*-

from django import forms
from app.user.forms import LoginForm
from django.contrib.auth import authenticate
from .models import Manager
from django.utils.translation import ugettext as _

__all__ = ['ManagerLoginForm', 'ManagerForm', 'ManagerUpdateForm']

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

class ManagerForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ManagerForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Нэвтрэх нэр'
		self.fields['email'].label = 'Э-мэйл'
		self.fields['groups'].label = 'Хандах эрх'
		self.fields['username'].help_text = None
		self.fields['groups'].help_text = None

	class Meta:
		model = Manager
		fields = ['username', 'email', 'groups']

		widgets = {
			'username' : forms.TextInput(attrs = {'class' : 'form-control'}),
			'email' : forms.EmailInput(attrs = {'class' : 'form-control'}),
			'groups' : forms.CheckboxSelectMultiple(),
		}

class ManagerUpdateForm(ManagerForm):

	def __init__(self, *args, **kwargs):
		super(ManagerUpdateForm, self).__init__(*args, **kwargs)
		self.fields['username'].disabled = True
		self.fields['email'].disabled = True