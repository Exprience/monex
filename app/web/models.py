# -*- coding:utf-8 -*-
import re

from django.db import models
from redactor.fields import RedactorField
from app.manager.models import Manager
__all__ = ['MedeeAngilal', 'Medee', 'SudalgaaAngilal', 'Sudalgaa', 'SurgaltAngilal',
			'Surgalt', 'BidniiTuhai', 'HolbooBarih', 'EconomicCalendar']

# Мэдээ
class MedeeAngilal(models.Model):
	name = models.CharField(max_length = 250, verbose_name = u"Мэдээ ангилал")

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
		ordering = ['-id']

	def __unicode__(self):
		return unicode(self.angilal)

	def img_url(self):
		path = re.compile(r'<img [^>]*src="([^"]+)')
		url = path.findall(self.body)
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
	pdf_file = models.FileField(verbose_name = u'Файл')

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

