# -*- coding:utf-8 -*-
from django import forms
from .models import SystemUser
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm



__all__ = ['RegisterForm', 'LoginForm', 'ProfileUpdateForm']


forms.Field.default_error_messages = {
    'required': u"Энэ талбарыг бөглөнө үү.",
}

class UserPasswordResetForm(PasswordResetForm):

	def __init__(self, *args, **kwargs):
		super(UserPasswordResetForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs['class'] = 'form-control'
		self.fields['email'].widget.attrs['placeholder'] = 'Э-мэйл'

class UserPasswordChangeForm(PasswordChangeForm):

	def __init__(self, *args, **kwargs):
		super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
		self.fields['old_password'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['old_password'].widget.attrs['placeholder'] = 'Хуучин нууц үг'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Шинэ нууц үг'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Шинэ нууц үг давтах'

class LoginForm(forms.Form):
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
		cleaned_data = super(LoginForm, self).clean()
		if self.is_valid():
			user = authenticate(username = cleaned_data['username'], password = cleaned_data['password'])
			if not user:
				raise forms.ValidationError(_(u'Хэрэглэгчийн нэр эсвэл нууц үг буруу байна'), code='invalid')
			else:
				if not SystemUser.objects.filter(username = user.username):
					raise forms.ValidationError(_(u'Хэрэглэгчийн нэр эсвэл нууц үг буруу байна'), code='invalid')
		return cleaned_data


class RegisterForm(forms.Form):
	username = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Нэвтрэх нэр'}) )
	email = forms.EmailField(widget = forms.EmailInput(attrs = {'class':'form-control', 'placeholder':'Э-мэйл'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':'Нууц үг'}))
	repeat_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':'Нууц үг давтах'}))

	#class Meta:
		#model = SystemUser
	#	fields = ['username', 'first_name', 'last_name', 'register', 'email', 'phone'] #'bank', 'account', 'password']
	#	widgets = {
	#		'username' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Нэвтрэх нэр'}),
	#		'first_name' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Нэр'}),
	#		'last_name' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Овог'}),
	#		'register' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Регистер'}),
	#		'email' : forms.EmailInput(attrs = {'class':'form-control', 'placeholder':'Э-мэйл'}),
	#		'phone' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Утас'}),
			#'bank' : forms.Select(attrs = {'class':'form-control', 'placeholder':'Банк'}),
			#'account' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Дансны дугаар'}),
			#'password' : forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':'Нууц үг'}),
	#	}
		

	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		if self.is_valid():
			password = cleaned_data['password']
			repeat_password = cleaned_data['repeat_password']
			if not password == repeat_password:
				raise forms.ValidationError(_(u'Нууц үг зөрүүтэй байна'), code='invalid')
		return cleaned_data



class ProfileUpdateForm(forms.Form):
	class Meta(RegisterForm):
		exclude = ['password']
