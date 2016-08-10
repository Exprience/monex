# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Manager(User):
	manager_status = models.BooleanField(default = False)
