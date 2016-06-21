# -*- coding:utf-8 -*-
import re
from django.db import models
from app.user.models import Bank
from redactor.fields import RedactorField
from app.manager.models import Manager
from datetime import datetime

__all__ = ['MedeeAngilal', 'Medee', 'SudalgaaAngilal', 'Sudalgaa', 'SurgaltAngilal',
			'Surgalt', 'BidniiTuhai', 'HolbooBarih', 'EconomicCalendar', 'Currency', 'CurrencyValue']

# Мэдээ
class MedeeAngilal(models.Model):
	name = models.CharField(max_length = 250, verbose_name = u"Мэдээ ангилал")

	class Meta:
		verbose_name_plural = u'Мэдээ ангилал'

	def __unicode__(self):
		return unicode(self.name)



class Medee(models.Model):
	angilal = models.ForeignKey(MedeeAngilal, verbose_name = u'Ангилал')
	title = models.CharField(max_length = 250, verbose_name = u'Гарчиг')
	body = RedactorField(verbose_name = u'Мэдээ')
	created_by = models.ForeignKey(Manager, null = True, blank = True)
	created_at = models.DateTimeField(auto_now_add = True)
	view = models.SmallIntegerField(default = 0)

	class Meta:
		verbose_name_plural = u'Мэдээ'
		ordering = ['-id']

	def __unicode__(self):
		return unicode(self.angilal)

	def img_url(self):
		path = re.compile(r'<img [^>]*src="([^"]+)')
		url = path.findall(self.body)
		if url:
			return url[0]

	def remove_html(self):
		p = re.compile(r'<.*?>')
		return p.sub('', self.body)

# Судалгаа
class SudalgaaAngilal(models.Model):
	name = models.CharField(max_length = 250, verbose_name = u'Ангилал')

	def __unicode__(self):
		return unicode(self.name)


class Sudalgaa(models.Model):
	angilal = models.ForeignKey(SudalgaaAngilal, verbose_name = u'Ангилал')
	name = models.CharField(max_length = 100, verbose_name = u'Нэр')
	author_name = models.CharField(max_length = 100, verbose_name = u'Судалгаа хийсэн')
	author_email = models.EmailField(verbose_name = 'Э-мэйл')
	pdf_file = models.FileField(verbose_name = u'Файл')
	date = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return unicode(self.name)

#Сургалт
class SurgaltAngilal(models.Model):
	name = models.CharField(max_length = 250, verbose_name = u'Ангилал')

	def __unicode__(self):
		return unicode(self.name)


class Surgalt(models.Model):
	angilal = models.ForeignKey(SurgaltAngilal, verbose_name = u'Ангилал')
	video_name = models.CharField(max_length = 200, null = True, verbose_name = u'Видео нэр')
	url = models.URLField(null = True, blank = True, verbose_name = u'Видео')
	author_name = models.CharField(max_length = 100, verbose_name = u'Хичээл заасан багш')
	author_email = models.EmailField(verbose_name = u'Хичээл заасан багшийн э-мэйл')
	created_at = models.DateTimeField(auto_now_add = True)

	def image(self):
		return "http://img.youtube.com/vi/%s/0.jpg" %self.url[32:]

	def __unicode__(self):
		return unicode(self.author_name)


class BidniiTuhai(models.Model):
	body = RedactorField()
	video_url = models.URLField(null = True, blank = True)

	def __unicode__(self):
		return unicode(self.video_url)

	def image(self):
		return "http://img.youtube.com/vi/%s/0.jpg" %self.video_url[32:]


class HolbooBarih(models.Model):
	body  = RedactorField()

	def __unicode__(self):
		return unicode(self.body)


class EconomicCalendar(models.Model):
	cur_select = (
		('0', u'Мон'),
		)
	imp_select = (
		('0', u'Амралт'),
		('1', u'1'),
		('2', u'2'),
		('3', u'3'),
		)
	time = models.DateTimeField()
	cur = models.CharField(choices = cur_select, max_length = 250)
	imp = models.CharField(choices = imp_select, max_length = 250)
	event = models.CharField(max_length = 250)
	actual = models.FloatField()
	forecast = models.FloatField()
	previous = models.FloatField()


class Currency(models.Model):
	bill = models.CharField(max_length = 50, verbose_name = u'Валют')
	icon = models.ImageField(null = True)

	class Meta:
		verbose_name_plural = u'Валют'

	def __unicode__(self):
		return unicode(self.bill)

class CurrencyValue(models.Model):
	bank = models.ForeignKey(Bank, verbose_name = u'Банк')
	currency = models.ForeignKey(Currency, verbose_name = 'Валют')
	buy = models.FloatField(verbose_name = u'Авах')
	sell = models.FloatField(verbose_name = u'Зарах')
	date = models.DateTimeField(auto_now_add = True)

	class Meta:
		verbose_name_plural = u'Валютийн ханш'

	def __unicode__(self):
		return u'%s | %s | %s | %s' %(self.bank, self.currency, self.buy, self.sell)