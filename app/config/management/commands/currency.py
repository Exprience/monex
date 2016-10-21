#!/usr/bin/env python
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

		models.Currency.objects.create(currency = 2, name = u"USDEUR", buy = float(data["rates"]["EUR"]), sell = float(data["rates"]["EUR"]) + float("%.6f" % (random.random())))
		#eur_buy  = float(data["rates"]["EUR"])
		#eur_sell = eur_buy + float("%.6f" %(random.random()))
		#print eur_buy
		#print eur_sell
		#mm.currency_create("7", "1", "2", str(eur_buy), str(eur_sell))
		models.Currency.objects.create(currency = 1, name = u"USDMNT", buy = float(data["rates"]["MNT"]), sell = float(data["rates"]["MNT"]) + float("%.6f" % (random.random())))
		models.Currency.objects.create(currency = 4, name = u"USDJPY", buy = float(data["rates"]["JPY"]), sell = float(data["rates"]["JPY"]) + float("%.6f" % (random.random())))
		models.Currency.objects.create(currency = 3, name = u"USDKRW", buy = float(data["rates"]["KRW"]), sell = float(data["rates"]["KRW"]) + float("%.6f" % (random.random())))
		models.Currency.objects.create(currency = 5, name = u"USDRUB", buy = float(data["rates"]["RUB"]), sell = float(data["rates"]["RUB"]) + float("%.6f" % (random.random())))