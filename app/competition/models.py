# -*- coding:utf-8 -*-

from django.db import models
from app.user.models import SystemUser
from simple_history.models import HistoricalRecords
from datetime import datetime
# Create your models here.

# Тэмцээний model үүсгэх
class CompetitionRank(models.Model):
	name = models.CharField(max_length = 100, verbose_name = u'Нэр')
	fee = models.IntegerField(verbose_name = u'Суурь хураамж')
	shagnal = models.TextField(verbose_name = u'Шагналын сан')
	history = HistoricalRecords()
	class Meta:
		ordering = ['-id']

	def __unicode__(self):
		return unicode(self.name)


class Competition(models.Model):

	competition_select = (
		('0', u'Бүртгэл эхэлсэн'),
		('1', u'Эхэлсэн'),
		('2', u'Дууссан'),
		)
	rank = models.ForeignKey(CompetitionRank, verbose_name = u'Ангилал')
	start = models.DateTimeField(verbose_name = u'Эхлэх огноо')
	end = models.DateTimeField(verbose_name = u'Дуусах огноо')
	status = models.BooleanField(default = False)
	competition_status = models.CharField(choices = competition_select, max_length = 10, default = '0', verbose_name = 'Төлөв')
	history = HistoricalRecords()

	def started(self):
		if self.competition_status in ['1', '2']:
			return True
		return False

	def last_ranked(self):
		return self.rank.history.as_of(self.history.first().history_date)

	def historys(self):
		return self.history.first()

	def if_registered(self):
		return self.competitionregister_set.all()

	def __unicode__(self):
		return unicode(self.rank)

class CompetitionRegister(models.Model):
	user = models.ForeignKey(SystemUser)
	competition = models.ForeignKey(Competition)
	status = models.BooleanField(default = False)
	account = models.IntegerField()
	barimt = models.ImageField()
	history = HistoricalRecords()

	def auto_increment(self):
		a = CompetitionRegister.objects.count()
		if a == None:
			self.account = 10000001
		else:
			self.account = 10000001 + a

	def __unicode__(self):
		return unicode(self.user)


# temtseen uusgeh model duusav