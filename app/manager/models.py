# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from datetime import datetime


from django.db import models

CREATE = ['4', '5', '6', '7']
UPDATE = ['2', '3', '6', '7']
DELETE = ['1', '3', '5', '7']
SELECT = '0'




class Manager(object):

	def fill_manager(self, result):
		#try:
		for key in result.__keylist__:
			if key == "last_login":
				if result.last_login._isNull == "true":
					self.last_login = None
				else:
					self.last_login = datetime.strptime(result.last_login.value, "%Y-%m-%d %H:%M:%S.%f")
			else:
				setattr(self, key, getattr(result, key).value)
		#except:
		#	pass

	def is_authenticated(self):
		return True

	def is_news_create(self):
		if self.news in CREATE:
			return True
		return False

	def is_news_update(self):
		if self.news in UPDATE:
			return True
		return False

	def is_news_delete(self):
		if self.news in DELETE:
			return True
		return False

	def is_news_select(self):
		if self.news != SELECT:
			return True
		return False

	def is_lesson_create(self):
		if self.news in CREATE:
			return True
		return False

	def is_lesson_update(self):
		if self.news in UPDATE:
			return True
		return False

	def is_lesson_delete(self):
		if self.news in DELETE:
			return True
		return False

	def is_lesson_select(self):
		if self.news != SELECT:
			return True
		return False

	def is_research_create(self):
		if self.news in CREATE:
			return True
		return False

	def is_research_update(self):
		if self.news in UPDATE:
			return True
		return False

	def is_research_delete(self):
		if self.news in DELETE:
			return True
		return False

	def is_research_select(self):
		if self.news != SELECT:
			return True
		return False

	def is_bank_create(self):
		if self.bank in CREATE:
			return True
		return False

	def is_bank_update(self):
		if self.bank in UPDATE:
			return True
		return False

	def is_bank_delete(self):
		if self.bank in DELETE:
			return True
		return False

	def is_bank_select(self):
		if self.bank != SELECT:
			return True
		return False

	def is_currency_create(self):
		if self.currency in CREATE:
			return True
		return False

	def is_currency_update(self):
		if self.currency in UPDATE:
			return True
		return False

	def is_currency_delete(self):
		if self.currency in DELETE:
			return True
		return False

	def is_currency_select(self):
		if self.currency != SELECT:
			return True
		return False

	def is_stock_create(self):
		if self.stock in CREATE:
			return True
		return False

	def is_stock_update(self):
		if self.stock in UPDATE:
			return True
		return False

	def is_stock_delete(self):
		if self.stock in DELETE:
			return True
		return False

	def is_stock_select(self):
		if self.stock != SELECT:
			return True
		return False


	def is_manager(self):
		return True

	def is_staff(self):
		return True

	def is_active(self):
		return True


class CompetitionRegister(models.Model):
	reciept = models.ImageField(verbose_name = u'Баримт')

	def __unicode__(self):
		return unicode(self.reciept)


class ResearchModel(models.Model):
	file = models.FileField()