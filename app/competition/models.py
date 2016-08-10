# -*- coding:utf-8 -*-
from django.db import models
from app.user.models import SystemUser
from datetime import datetime
from monex.get_username import get_username
from .token import competition_register_token as c
from django.core.urlresolvers import reverse
# Create your models here.

# Тэмцээний model үүсгэх
class CompetitionRank(models.Model):
	name = models.CharField(max_length = 100, verbose_name = u'Нэр')
	fee = models.IntegerField(verbose_name = u'Суурь хураамж')
	shagnal = models.TextField(verbose_name = u'Шагналын сан')
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
	

	@property
	def user(self):
		request_user = get_username().user
		return request_user

	def started(self):
		if self.competition_status in ['1', '2']:
			return True
		return False

	def last_ranked(self):
		return self.rank.history.as_of(self.history.first().history_date)

	def historys(self):
		return self.history.first()

	def if_registered(self):
		user = self.user
		for i in self.competitionregister_set.all():
			if i.user.id == user.id:
				return True
		return False

	def get_url(self):
		if self.if_registered():
			register = CompetitionRegister.objects.get(user__id = self.user.id, competition__id = self.id)
			url = c.encode(self.user.id, self.id, register.id, register.registered_date)
			return reverse('competition:competition_home', args = [url])
		else:
			return False
		
	@classmethod
	def registered_competition(self, user):
		competition_list = []
		system_user = SystemUser.objects.get(id = user.id)
		competition_register_list = CompetitionRegister.objects.filter(user = system_user)
		for i in competition_register_list:
			competition_list.append(i.competition)
		return competition_list

	def __unicode__(self):
		return unicode(self.rank)

class CompetitionRegister(models.Model):
	user = models.ForeignKey(SystemUser)
	competition = models.ForeignKey(Competition)
	status = models.BooleanField(default = False)
	account = models.IntegerField()
	barimt = models.FileField(verbose_name = u'Баримт')
	registered_date = models.DateTimeField(auto_now_add = True)
	
	class Meta:
		unique_together = (('user', 'competition'),)

	def auto_increment(self):
		a = CompetitionRegister.objects.count()
		if a == None:
			self.account = 10000001
		else:
			self.account = 10000001 + a

	def __unicode__(self):
		return unicode(self.user.username)



# temtseen uusgeh model duusav