# -*- coding:utf-8 -*-

from django import forms
from redactor.widgets import RedactorEditor
from .models import *
from app.manager.forms import RelAdd
from django.contrib.admin.sites import AdminSite
my_admin_site = AdminSite(name='manager_rank_create')
__all__ = ['BagtsForm', 'NewsForm', 'AboutForm', 'LessonForm', 'ResearchForm', 'NewsCategoryForm']

class BagtsForm(forms.Form):
	name = forms.CharField(label = u'Хувьцааны нэр', widget = forms.TextInput(attrs = {'class':'form-control'}))
	avsan_une = forms.FloatField(label = u'Авсан үнэ', widget = forms.TextInput(attrs = {'class':'form-control'}))
	zarsan_une = forms.FloatField(label = u'Зарсан үнэ', widget = forms.TextInput(attrs = {'class':'form-control'}))
	too = forms.IntegerField(label = u'Ширхэг', widget = forms.TextInput(attrs = {'class':'form-control'}))

class NewsForm(forms.ModelForm):
	
	class Meta:
		model = Medee
		fields = ['angilal', 'title', 'body']

		widgets = {
			'angilal' : RelAdd(
				Medee._meta.get_field('angilal').formfield().widget,
            	Medee._meta.get_field('angilal').rel,
            	my_admin_site,
            	can_add_related=True,
            	can_change_related = True,
            	),
			'title' : forms.TextInput(attrs = {'class':'form-control'})
		}

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

	class Meta:
		model = Sudalgaa
		fields = "__all__"
		widgets = {
			'angilal' : RelAdd(
				Sudalgaa._meta.get_field('angilal').formfield().widget,
            	Sudalgaa._meta.get_field('angilal').rel,
            	my_admin_site,
            	can_add_related=True,
            	can_change_related = True,
            	),
			'name' : forms.TextInput(attrs = {'class':'form-control'}),
			'author_name' : forms.TextInput(attrs = {'class':'form-control'}),
			'pdf_file' : forms.FileInput(attrs = {'class':'form-control'}),

		}

class NewsCategoryForm(forms.ModelForm):

	class Meta:
		model = MedeeAngilal
		fields = "__all__"
		widgets = {
			'name' : forms.TextInput(attrs = {'class':'form-control'})
		}