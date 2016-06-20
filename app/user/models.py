# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

__all__ = ['SystemUser']


class Bank(models.Model):
	name = models.CharField(max_length = 200)

	def __unicode__(self):
		return unicode(self.name)


class SystemUser(User):

	register = models.CharField(max_length = 10, verbose_name = u'Регистер:', unique = True, null = True)
	phone = models.IntegerField(verbose_name = u'Утас:', null = True)
	bank = models.ForeignKey(Bank, verbose_name = 'Банк:', null = True)
	account = models.IntegerField(verbose_name = 'Дансний дугаар:', null = True)
	
	def __unicode__(self):
		return unicode(self.first_name)