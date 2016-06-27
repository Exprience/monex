
from django import forms
from .models import SupportMessage

class SupportUserMessageForm(forms.ModelForm):

	class Meta:
		model = SupportMessage
		fields = ['system_user_message']
		widgets = {
			'system_user_message': forms.TextInput(attrs = {'class':'form-control'})
		}

class SupportManagerMessageForm(forms.ModelForm):

	class Meta:
		model = SupportMessage
		fields = ['manager_message']
		widgets = {
			'manager_message': forms.TextInput(attrs = {'class':'form-control'})
		}
