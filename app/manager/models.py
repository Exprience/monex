# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Manager(User):
	manager_status = models.BooleanField(default = False)
	history = HistoricalRecords()
	
