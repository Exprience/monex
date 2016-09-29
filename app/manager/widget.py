# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class PopUpWidget(forms.Widget):
	
	template = 'manager/related.html'
	
	def __init__(self, widget, value, can_add_related = False, can_change_related = False, can_delete_related = False):
		self.can_change_related = can_change_related
		self.can_add_related = can_add_related
		self.can_delete_related = can_delete_related
		self.widget = widget
		self.attrs = self.widget.attrs
		self.value = value


	def render(self, name, value, attrs=None, choices=(), *args, **kwargs):
		context = {
			'widget': self.widget.render(name, value, *args, **kwargs),
			}

		if self.can_change_related:
			change_related_url = self.get_related_url('update', value)
			context.update(
				can_change_related=True,
				change_related_url=change_related_url,
			)

		if self.can_add_related:
			add_related_url = self.get_related_url('create', value)
			context.update(
				can_add_related=True,
				add_related_url=add_related_url,
			)
		if self.can_delete_related:
			delete_related_url = self.get_related_url('delete', value)
			context.update(
				can_delete_related=True,
				delete_related_url=delete_related_url,
			)
		return mark_safe(render_to_string(self.template, context))

	def get_related_url(self, type, value):
		if type == "create":
			return reverse_lazy("manager:%s_category_%s" %(self.value, type))
		else:
			if value:
				return reverse_lazy("manager:%s_category_%s" %(self.value, type), kwargs = {'pk': value})
			else:
				return reverse_lazy("manager:%s_category_%s" %(self.value, type), kwargs = {'pk': self.widget.choices[0][0]})