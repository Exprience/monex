# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django.views import generic as g


class Home(g.TemplateView):
	template_name = 'competition/home.html'
class lol (g.TemplateView):
	template_name = 'competition/popup.html'