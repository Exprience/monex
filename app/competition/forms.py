from django import forms
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

#from django.utils.safestring import mark_safe
#from django.conf import settings


from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.contrib.admin.sites import AdminSite



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


class CompetitionRankForm(forms.Form):
	pass


class CompetitionForm(forms.Form):
	pass



class CompetitionRegisterForm(forms.Form):
	pass

