# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _


from app.user.forms import UserLoginForm





class ManagerLoginForm(UserLoginForm):

	def clean(self):
		cleaned_data = super(ManagerLoginForm, self).clean()
		if self.is_valid():
			user = authenticate(username = cleaned_data['username'], password = cleaned_data['password'])
			if not user:
				raise forms.ValidationError(_(u'Хэрэглэгчийн нэр эсвэл нууц үг буруу байна'), code='invalid')
			else:
				if not Manager.objects.filter(username = user.username):
					raise forms.ValidationError(_(u'Хэрэглэгчийн нэр эсвэл нууц үг буруу байна'), code='invalid')
		return cleaned_data




class ManagerForm(forms.Form):

	pass




class ManagerUpdateForm(ManagerForm):

	pass