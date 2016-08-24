# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib import messages


from app.config.get_username import get_username as gu
from managers import BaseDataManager as manager


forms.Field.default_error_messages = {
    'required': u"Энэ талбарыг бөглөнө үү.",
}




class UserPasswordResetForm(forms.Form):
	email = forms.EmailField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Э-мэйл хаяг'}))

	def clean(self):
		if self.is_valid():
			cleaned_data = super(UserPasswordResetForm, self).clean()
			email = cleaned_data['email']
			if not User.objects.filter(email = email):
				raise forms.ValidationError(_('Э-мэйл хаяг бүртгэлгүй байна'), code='invalid')
			return cleaned_data




class UserPasswordChangeForm(forms.Form):

	old_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Хуучин нууц үг'}))
	new_password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Шинэ нууц үг'}))
	new_password2	 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Шинэ нууц үг давтах'}))


	def clean(self):
		cleaned_data = super(UserPasswordChangeForm, self).clean()
		if self.is_valid():
			if cleaned_data['new_password1'] != cleaned_data['new_password2']:
				raise forms.ValidationError(_('Нууц үг таарахгүй байна'))
		return cleaned_data




class UserSetPasswordForm(forms.Form):

	def __init__(self, *args , **kwargs):
		super(UserSetPasswordForm, self).__init__(*args, **kwargs)
		self.fields['new_password1'].widget.attrs['placeholder'] = u'Нууц үг'
		self.fields['new_password2'].widget.attrs['placeholder'] = u'Нууц үг давтах'
		self.fields['new_password1'].widget.attrs['class'] = u'form-control'
		self.fields['new_password2'].widget.attrs['class'] = u'form-control'

	def save(self, *args, **kwargs):
		messages.success(gu(), _('Нууц үг амжилттай хадгалагдлаа'))
		return super(UserSetPasswordForm, self).save(*args, **kwargs)




class UserLoginForm(forms.Form):
	username = forms.CharField(label = u"Нэвтрэх нэр:", widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Нэвтрэх нэр'}))
	password = forms.CharField(label = u"Нууц үг:", widget = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'Нууц үг'}))
	remember_me = forms.BooleanField(required = False, initial = True, label = 'Намайг сана')

	def clean_remember_me(self):
		remember_me = self.cleaned_data['remember_me']
		if not remember_me:
			settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
		else:
			settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
		return remember_me


	def clean(self):
		cleaned_data = super(UserLoginForm, self).clean()
		if self.is_valid():
			user = manager.loginUser(cleaned_data['username'], cleaned_data['password'])
			if user is None:
				raise forms.ValidationError(_(u'Хэрэглэгчийн нэр эсвэл нууц үг буруу байна'), code='invalid')
		return cleaned_data




class UserRegisterForm(forms.Form):
	username = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Нэвтрэх нэр'}) )
	email = forms.EmailField(widget = forms.EmailInput(attrs = {'class':'form-control', 'placeholder':'Э-мэйл'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':'Нууц үг'}))
	repeat_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':'Нууц үг давтах'}))
		


	def clean_username(self):
		username = self.cleaned_data['username']
		print manager.check_unique_user(True, username)
		if not manager.check_unique_user(True, username):
			raise forms.ValidationError(_(u'Хэрэглэгч бүртгэлтэй байна'), code='invalid')
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if not manager.check_unique_user(False, email):
			raise forms.ValidationError(_(u'Э-мэйл хаяг бүртгэлтэй байна'), code='invalid')
		return email

	def clean(self):
		cleaned_data = super(UserRegisterForm, self).clean()
		if self.is_valid():
			password = cleaned_data['password']
			repeat_password = cleaned_data['repeat_password']
			if not password == repeat_password:
				raise forms.ValidationError(_(u'Нууц үг зөрүүтэй байна'), code='invalid')
		return cleaned_data