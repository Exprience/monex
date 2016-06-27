from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
from app.user.models import Bank
from app.web.models import Company
from .token import competition_register_token as c
from .models import CompetitionRegister
# Create your views here.

class CompetitionHome(TemplateView):
	template_name = 'competition/home/home.html'

	def dispatch(self, request, *args, **kwargs):
		tokenize = self.kwargs['token']
		if c.check_token(request.user.id, tokenize):
			token = c.decode(tokenize)
			if CompetitionRegister.objects.filter(
				user__id = token['user_id'],
				competition__id = token['competition_id'],
				id = token['register_id'],
				registered_date__startswith = token['registered_date']
				):
				return super(CompetitionHome, self).dispatch(request, *args, **kwargs)
			else:
				raise Http404
		else:
			raise Http404
	def get_context_data(self, *args, **kwargs):
		context = super(CompetitionHome, self).get_context_data(*args, **kwargs)
		context['banks'] = Bank.objects.currency_bank()
		context['companys'] = Company.objects.all()
		return context
