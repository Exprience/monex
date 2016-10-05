# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django import forms
from django.conf import settings


from managers import UserDataManager as um
from app.config import config


class PasswordResetForm(forms.Form):
	email = forms.EmailField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Э-мэйл хаяг'}))

	def clean(self):
		if self.is_valid():
			cleaned_data = super(UserPasswordResetForm, self).clean()
			email = cleaned_data['email']
			if not User.objects.filter(email = email):
				raise forms.ValidationError(u'Э-мэйл хаяг бүртгэлгүй байна', code='invalid')
			return cleaned_data


class PasswordChangeForm(forms.Form):

	old_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Хуучин нууц үг'}))
	new_password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Шинэ нууц үг'}))
	new_password2	 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Шинэ нууц үг давтах'}))


	def clean(self):
		cleaned_data = super(UserPasswordChangeForm, self).clean()
		if self.is_valid():
			if cleaned_data['new_password1'] != cleaned_data['new_password2']:
				raise forms.ValidationError(u'Нууц үг таарахгүй байна')
		return cleaned_data


class SetPasswordForm(forms.Form):
	new_password1 = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Нууц үг'}))
	new_password2 = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Нууц үг давтах'}))


class LoginForm(forms.Form):
	username = forms.CharField(label = u"", widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Нэвтрэх нэр'}))
	password = forms.CharField(label = u"", widget = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'Нууц үг'}))
	remember_me = forms.BooleanField(required = False, initial = True, label = 'Намайг сана')

	def clean_remember_me(self):
		remember_me = self.cleaned_data['remember_me']
		if not remember_me:
			settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
		else:
			settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
		return remember_me


class RegisterForm(forms.Form):
	username = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Нэвтрэх нэр'}) )
	email = forms.EmailField(widget = forms.EmailInput(attrs = {'class':'form-control', 'placeholder':'Имэйл'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':'Нууц үг'}))
	repeat_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':'Нууц үг давтах'}))

	def clean_username(self):
		username = self.cleaned_data['username']
		self.error(username, True)
		return username

	def clean_email(self):
		email = self.cleaned_data["email"]
		self.error(email, False)
		return email

	def error(self, value, status):
		result = um.check_unique_user(status, value)
		if not result:
			raise forms.ValidationError(config.UNIQUE_USERNAME, code='invalid')
		if result == config.URL_ERROR:
			raise forms.ValidationError(config.URL_ERROR_MESSAGE, code='invalid')
		if result == config.SYSTEM_ERROR:
			raise forms.ValidationError(config.SYSTEM_ERROR_MESSAGE, code='invalid')

	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		if self.is_valid():
			password = cleaned_data['password']
			repeat_password = cleaned_data['repeat_password']
			if not password == repeat_password:
				raise forms.ValidationError(_(u'Нууц үг зөрүүтэй байна'), code='invalid')
		return cleaned_data 