from datetime import datetime
from django.db import models

from app.user.models import SystemUser
from app.manager.models import Manager

class Support(models.Model):
	manager = models.ForeignKey(Manager)
	system_user = models.ForeignKey(SystemUser)

	def __unicode__(self):
		return u"%s | %s" %(self.manager.username, self.system_user.username)

class SupportMessage(models.Model):
	support = models.ForeignKey(Support)
	manager_message = models.CharField(max_length = 250, null = True)
	system_user_message = models.CharField(max_length = 250, null = True, blank = True)
	support_date = models.DateTimeField(auto_now_add = True, blank = True)
	read_at = models.DateTimeField(null = True)

	def reading(self):
		if not self.read_at:
			return False
		return True
