# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
from redactor.widgets import RedactorEditor

#from django.core.urlresolvers import reverse_lazy

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from app.manager.managers import ManagerBaseDataManager

#Export
__all__ = []


class BagtsForm(forms.Form):
	name = forms.CharField(label = u'Хувьцааны нэр', widget = forms.TextInput(attrs = {'class':'form-control'}))
	avsan_une = forms.FloatField(label = u'Авсан үнэ', widget = forms.TextInput(attrs = {'class':'form-control'}))
	zarsan_une = forms.FloatField(label = u'Зарсан үнэ', widget = forms.TextInput(attrs = {'class':'form-control'}))
	too = forms.IntegerField(label = u'Ширхэг', widget = forms.TextInput(attrs = {'class':'form-control'}))


class LessonCategoryForm(forms.Form):

	pass


class ResearchCategoryForm(forms.Form):

	name = forms.CharField(label = u'Гарчиг', widget = forms.TextInput(attrs = {'class':'form-control'}))


class LessonMailForm(forms.Form):
	feedback = forms.CharField(widget = forms.Textarea(attrs = {'class':'form-control'}), label = u'Санал хүсэлт')
	captcha = CaptchaField()