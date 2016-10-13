# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import urllib2
import json
import random


from django.core.management import BaseCommand
from app.manager.managers import ManagerDataManager as mm
from app.manager import models



class Command(BaseCommand):

	help = "My test command"

	def handle(self, *args, **options):
		
		response = urllib2.urlopen("https://openexchangerates.org/api/latest.json?app_id=10c73ccb4d0a43d988c8ab011fd90bf2")
		data = json.load(response)

		change =  float("%.6f" % (random.random()))
		buy = float(data["rates"]["EUR"])
		sell = buy + change

		models.Currency.objects.create(currency = 1, name = u"USDEUR", buy = buy , sell = sell)