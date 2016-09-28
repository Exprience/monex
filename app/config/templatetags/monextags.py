# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django.template.defaulttags import register
from django.utils.safestring import mark_safe

from app.web.managers import WebBaseDataManager as wm

@register.simple_tag()
def get_competition_status_label(value):
	if value == "1":
		return "success"
	elif value == "2":
		return "info"
	elif value == "3":
		return "warning"
	elif value == "4":
		return "primary"
	return True


@register.simple_tag()
def get_competition_status(value):
	if value == "1":
		return u"Бүртгэл эхэлсэн"
	if value == "2":
		return u"Эхэлсэн"
	if value == "3":
		return u"Миний тэмцээн"
	if value == "4":
		return u"Дууссан"
	return True


@register.simple_tag()
def if_registered(competition_id, user_id, status):
	result = wm.if_register(competition_id, user_id)
	if result:
		if status == "2":
			return mark_safe(u"<a href='/platform/%s' class='btn btn-primary btn-xs btn-flat'>Тоглох</a>"%competition_id)
		elif status == "1":
			return u"Бүртгүүлсэн байна"
	else:
		#if status == "3":
		#	return "Тэмцээн дууссан байна"
		#elif status == "2":
		#	return "Тэмцээн эхэлсэн байна"
		if status == "1":
			return mark_safe(u"<a href='/competition/register/%s/' class='btn btn-success btn-xs btn-flat'>Бүртгүүлэх</a>" % competition_id)
	return ""