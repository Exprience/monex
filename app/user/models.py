# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

__all__ = ['SystemUser']


class Bank(models.Model):
	name = models.CharField(max_length = 200)
	icon = models.ImageField(null = True)

	class Meta:
		verbose_name_plural = u'Банк'
		
	def __unicode__(self):
		return unicode(self.name)

	def get_currency(self):
		#return self.currencyvalue_set.filter(date__startswith = datetime.now().date())
		return self.currencyvalue_set.all()


class SystemUser(User):

	register = models.CharField(max_length = 10, verbose_name = u'Регистер:', unique = True, null = True)
	phone = models.IntegerField(verbose_name = u'Утас:', null = True)
	bank = models.ForeignKey(Bank, verbose_name = 'Банк:', null = True)
	account = models.IntegerField(verbose_name = 'Дансний дугаар:', null = True)
	
	def __unicode__(self):
		return unicode(self.first_name)