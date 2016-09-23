# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
from app.manager.models import CompetitionRegister
#Export
__all__ = []


class BagtsForm(forms.Form):
	name = forms.CharField(label = u'Хувьцааны нэр', widget = forms.TextInput(attrs = {'class':'form-control'}))
	avsan_une = forms.FloatField(label = u'Авсан үнэ', widget = forms.TextInput(attrs = {'class':'form-control'}))
	zarsan_une = forms.FloatField(label = u'Зарсан үнэ', widget = forms.TextInput(attrs = {'class':'form-control'}))
	too = forms.IntegerField(label = u'Ширхэг', widget = forms.TextInput(attrs = {'class':'form-control'}))


class LessonMailForm(forms.Form):
	feedback = forms.CharField(widget = forms.Textarea(attrs = {'class':'form-control'}), label = u'Санал хүсэлт')
	captcha = CaptchaField()

class CompetitionRegisterForm(forms.ModelForm):
	
	class Meta:
		model = CompetitionRegister
		fields = ['reciept']