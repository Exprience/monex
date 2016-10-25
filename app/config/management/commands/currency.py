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

		eur_buy  = float(data["rates"]["EUR"])
		eur_sell = eur_buy + float("%.6f" %(random.random()))
		models.Currency.objects.create(currency = 2, name = u"USDEUR", buy = eur_buy, sell = eur_sell)
		mm.currency_create("7", "1", "2", str(eur_buy), str(eur_sell))

		mnt_buy  = float(data["rates"]["MNT"])
		mnt_sell = mnt_buy + float("%.6f" %(random.random()))
		models.Currency.objects.create(currency = 1, name = u"USDMNT", buy = mnt_buy, sell = mnt_sell)
		mm.currency_create("7", "1", "1", str(mnt_buy), str(mnt_sell))

		jpy_buy  = float(data["rates"]["JPY"])
		jpy_sell = jpy_buy + float("%.6f" %(random.random()))
		models.Currency.objects.create(currency = 4, name = u"USDJPY", buy = jpy_buy, sell = jpy_sell)
		mm.currency_create("7", "1", "4", str(jpy_buy), str(jpy_sell))

		krw_buy  = float(data["rates"]["KRW"])
		krw_sell = krw_buy + float("%.6f" %(random.random()))
		models.Currency.objects.create(currency = 3, name = u"USDKRW", buy = krw_buy, sell = krw_sell)
		mm.currency_create("7", "1", "3", str(krw_buy), str(krw_sell))

		rub_buy  = float(data["rates"]["RUB"])
		rub_sell = rub_buy + float("%.6f" %(random.random()))
		models.Currency.objects.create(currency = 5, name = u"USDRUB", buy = rub_buy, sell = rub_sell)
		mm.currency_create("7", "1", "5", str(rub_buy), str(rub_sell))