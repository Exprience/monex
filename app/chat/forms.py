# -*- coding:utf-8 -*-

from django import forms
from captcha.fields import CaptchaField
__all__ = ['RoomForm', 'MessageForm']


class RoomForm(forms.Form):
	pass

class MessageForm(forms.Form):
	pass
		