# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
from redactor.widgets import RedactorEditor


#Export
__all__ = []


class BagtsForm(forms.Form):
	name = forms.CharField(label = u'Хувьцааны нэр', widget = forms.TextInput(attrs = {'class':'form-control'}))
	avsan_une = forms.FloatField(label = u'Авсан үнэ', widget = forms.TextInput(attrs = {'class':'form-control'}))
	zarsan_une = forms.FloatField(label = u'Зарсан үнэ', widget = forms.TextInput(attrs = {'class':'form-control'}))
	too = forms.IntegerField(label = u'Ширхэг', widget = forms.TextInput(attrs = {'class':'form-control'}))




class NewsForm(forms.Form):
	ch = (
		(1,1),
		(2,2),
		(3,3),
		(4,4),
		)
	category = forms.ChoiceField(label = u'Ангилал',choices = ch,  widget = forms.Select(attrs = {'class':'form-control'}))
	
	title = forms.CharField(label = u'Гарчиг', widget = forms.TextInput(attrs = {'class':'form-control'}))
	body = forms.CharField(label = u'Мэдээ',widget = RedactorEditor(attrs = {'class':'form-control'}))
	



class LessonForm(forms.Form):
	video_name= forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control'}))
	url = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control'}))
	author_name = forms.ChoiceField(required=True)
	author_email = forms.EmailField(widget = forms.EmailInput(attrs = {'class':'form-control'}))
	category = forms.ChoiceField(required=True)




class ResearchForm(forms.Form):

	name = forms.CharField(label = u'нэр', widget = forms.TextInput(attrs = {'class':'form-control'}))
	



class NewsCategoryForm(forms.Form):

	angilal = forms.CharField(label = u'Ангилал', widget = forms.TextInput(attrs = {'class':'form-control'}))




class LessonCategoryForm(forms.Form):

	pass




class ResearchCategoryForm(forms.Form):

	pass




class ResearchCategoryForm(forms.Form):

	name = forms.CharField(label = u'Гарчиг', widget = forms.TextInput(attrs = {'class':'form-control'}))




class LessonMailForm(forms.Form):
	feedback = forms.CharField(widget = forms.Textarea(attrs = {'class':'form-control'}), label = u'Санал хүсэлт')
	captcha = CaptchaField()