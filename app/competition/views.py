from django.shortcuts import render
from django.views.generic import TemplateView

from app.user.models import Bank
from app.web.models import Company
# Create your views here.

class CompetitionHome(TemplateView):
	template_name = 'competition/home/home.html'

	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionHome, self).get_context_data(*args, **kwargs)
		context['banks'] = Bank.objects.currency_bank()
		context['companys'] = Company.objects.all()
		return context
