from __future__ import unicode_literals

from django.db import models

from app.user.models import SystemUser
from app.manager.models import Manager

class Support(models.Model):
	manager = models.ForeignKey(Manager)
	system_user = models.ForeignKey(SystemUser)

class SupportMessage(models.Model):
	support = models.ForeignKey(Support)
	manager_message = models.CharField(max_length = 250)
	system_user_message = models.CharField(max_length = 250)