# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from datetime import datetime


CREATE = ['4', '5', '6', '7']
UPDATE = ['2', '3', '6', '7']
DELETE = ['1', '3', '5', '7']
SELECT = '0'




class Manager(object):
	
	issuccess = ''
	last_login = None
	password = None

	def fill_manager(self, value):
		if hasattr(value, 'manager_id'):
			if value.manager_id != None:
				if hasattr(value.manager_id, 'value'):
					self.id = int(value.manager_id.value)
					self.pk = int(value.manager_id.value)
				else:
					self.id = int(value.manager_id)
					self.pk = int(value.manager_id)
		if hasattr(value, 'id'):
			if value.id != None:
				self.id = int(value.id.text)
				self.pk = int(value.id.text)			
		if hasattr(value, 'email'):
			if value.email != None:
				self.email = value.email.text
		if hasattr(value, 'is_superuser'):
			if value.is_superuser != None:
				if value.is_superuser.text == "1":
					self.is_superuser = True
				else:
					self.is_superuser = False
		if hasattr(value, 'is_active'):
			if value.is_active != None:
				self.is_active = value.is_active.text
		if hasattr(value, 'last_login'):
			if value.last_login != None:	
				if not value.last_login.text == '':
					self.last_login = datetime.strptime(value.last_login.text, "%Y-%m-%d %H:%M:%S.%f")
		if hasattr(value, 'news'):
			if value.news != None:
				self.news = value.news.text
		if hasattr(value, 'research'):
			if value.research != None:
				self.research = value.research.text
		if hasattr(value, 'lesson'):
			if value.lesson != None:
				self.lesson = value.lesson.text
		if hasattr(value, 'competition_type'):
			if value.competition_type != None:
				self.competition_type = value.competition_type.text
		if hasattr(value, 'competition'):
			if value.competition != None:
				self.competition = value.competition.text
		if hasattr(value, 'stock'):
			if value.stock != None:
				self.stock = value.stock.text
		if hasattr(value, 'bank'):
			if value.bank != None:
				self.bank = value.bank.text
		if hasattr(value, 'currency'):
			if value.currency != None:
				self.currency = value.currency.text
		if hasattr(value, 'competition_approval'):
			if value.competition_approval != None:
				self.competition_approval = value.competition_approval.text
		if hasattr(value, 'password'):
			if value.password != None:
				self.password = value.password.text

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

	def is_manager(self):
		return True