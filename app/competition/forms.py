from django import forms
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

#from django.utils.safestring import mark_safe
#from django.conf import settings


from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.contrib.admin.sites import AdminSite

from bootstrap3_datetime.widgets import DateTimePicker

from .models import CompetitionRank, Competition, CompetitionRegister

__all__ = ['CompetitionForm', 'CompetitionRankForm']


my_admin_site = AdminSite(name='manager_create')

class RelAdd(RelatedFieldWidgetWrapper):

	#template = 'manager/related.html'

	def __init__(self, *args, **kwargs):
		super(RelAdd, self).__init__(*args, **kwargs)
		self.admin_site = my_admin_site
		self.attrs['class'] = 'form-control'
		self.attrs['style'] = 'width:90%;' #= {'class' : 'form-control'}

	def get_related_url(self, info, action, *args):
		return reverse("manager:manager_%s_%s_%s" % (info + (action,)), args = args)


class CompetitionRankForm(forms.ModelForm):

	class Meta:
		model = CompetitionRank
		fields = "__all__"
		widgets = {
			'name' : forms.TextInput(attrs = {'class' : 'form-control'}),
			'fee' : forms.TextInput(attrs = {'class' : 'form-control'}),
			'shagnal' : forms.Textarea(attrs = {'class' : 'form-control'}),
		}

class CompetitionForm(forms.ModelForm):

	class Meta:
		model = Competition
		exclude = ['status', 'competition_status']
		widgets = {
			'rank' : RelAdd(
				Competition._meta.get_field('rank').formfield().widget,
            	Competition._meta.get_field('rank').rel,
            	my_admin_site,
            	can_change_related=True,
            	can_add_related=True,
            	), 
			'start' : DateTimePicker(options={"format": "YYYY-MM-DD HH:mm", "pickSeconds": False}),
			'end' : DateTimePicker(options={"format": "YYYY-MM-DD HH:mm", "pickSeconds": False}),
		}

class CompetitionRegisterForm(forms.ModelForm):

	class Meta:
		model = CompetitionRegister
		fields = ['barimt']
		widgets = {
			'barimt': forms.FileInput(attrs = {'class':'form-control'})
		}