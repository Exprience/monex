# -*- coding:utf-8 -*-

from django import forms
from .models import *
from app.competition.forms import RelAdd, my_admin_site
from captcha.fields import CaptchaField, CaptchaTextInput

__all__ = ['BagtsForm', 'NewsForm', 'AboutForm', 'LessonForm', 'ResearchForm', 'NewsCategoryForm',
			'LessonCategoryForm', 'ResearchCategoryForm']

class BagtsForm(forms.Form):
	name = forms.CharField(label = u'Хувьцааны нэр', widget = forms.TextInput(attrs = {'class':'form-control'}))
	avsan_une = forms.FloatField(label = u'Авсан үнэ', widget = forms.TextInput(attrs = {'class':'form-control'}))
	zarsan_une = forms.FloatField(label = u'Зарсан үнэ', widget = forms.TextInput(attrs = {'class':'form-control'}))
	too = forms.IntegerField(label = u'Ширхэг', widget = forms.TextInput(attrs = {'class':'form-control'}))

class NewsForm(forms.Form):
	
	#class Meta:
	#	model = Medee
	#	fields = ['angilal', 'title', 'body']

	#	widgets = {
	#		'angilal' : RelAdd(
	#			Medee._meta.get_field('angilal').formfield().widget,
    #        	Medee._meta.get_field('angilal').rel,
    #        	my_admin_site,
    #        	can_add_related=True,
    #        	can_change_related = True,
    #        	),
	#		'title' : forms.TextInput(attrs = {'class':'form-control'})
	#	}

class AboutForm(forms.ModelForm):

	class Meta:
		model = BidniiTuhai
		fields = "__all__"
		widgets = {
			'video_url' : forms.TextInput(attrs = {'class':'form-control'})
		}

class LessonForm(forms. ModelForm):

	class Meta:
		model = Surgalt
		fields = "__all__"
		widgets = {
			'angilal' : RelAdd(
				Surgalt._meta.get_field('angilal').formfield().widget,
            	Surgalt._meta.get_field('angilal').rel,
            	my_admin_site,
            	can_add_related=True,
            	can_change_related = True,
            	),
			'video_name' : forms.TextInput(attrs = {'class':'form-control'}),
			'url' : forms.TextInput(attrs = {'class':'form-control'}),
			'author_name' : forms.TextInput(attrs = {'class':'form-control'}),
			'author_email' : forms.EmailInput(attrs = {'class':'form-control'}),
			}

class ResearchForm(forms.ModelForm):

	#class Meta:
	#	model = Sudalgaa
	#	fields = "__all__"
	#	widgets = {
	#		'angilal' : RelAdd(
	#			Sudalgaa._meta.get_field('angilal').formfield().widget,
    #        	Sudalgaa._meta.get_field('angilal').rel,
    #        	my_admin_site,
    #        	can_add_related=True,
    #        	can_change_related = True,
    #        	),
	#		'name' : forms.TextInput(attrs = {'class':'form-control'}),
	#		'author_name' : forms.TextInput(attrs = {'class':'form-control'}),
	#		'author_email' : forms.TextInput(attrs = {'class' : 'form-control'}),
	#		'pdf_file' : forms.FileInput(attrs = {'class':'form-control'}),


	#	}

class NewsCategoryForm(forms.Form):
	name = forms.TextInput()
	#class Meta:
	#	model = MedeeAngilal
	#	fields = "__all__"
	#	widgets = {
	#		'name' : forms.TextInput(attrs = {'class':'form-control'})
	#	}

class LessonCategoryForm(forms.ModelForm):

	class Meta:
		model = SurgaltAngilal
		fields = "__all__"
		widgets = {
			'name' : forms.TextInput(attrs = {'class' : 'form-control'})
		}

class ResearchCategoryForm(forms.ModelForm):

	class Meta:
		model = SudalgaaAngilal
		fields = "__all__"
		widgets = {
			'name' : forms.TextInput(attrs = {'class' : 'form-control'})
		}

class LessonMailForm(forms.Form):
	feedback = forms.CharField(widget = forms.Textarea(attrs = {'class':'form-control'}), label = u'Санал хүсэлт')
	captcha = CaptchaField()