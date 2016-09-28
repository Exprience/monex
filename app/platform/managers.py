# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from app.config.managers import BaseDataManager
from django.conf import settings
from app.config import config

class PlatformBaseDataManager(BaseDataManager):
	
	@staticmethod
	def currency(type, competition_id, user_id, piece, value_id, id = 1, isCurrency = True, isManager = False, manager_id = ""):
		client = PlatformBaseDataManager.get_instance().setup_client('%ssoap/platform/buy_sell/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
		
		currencyR = client.factory.create('ns0:MXUserShowCurrencyCUS_ResponseR')
		currency = client.factory.create('ns0:MXUserShowCurrencyCUS_Response')
		currencyRecord = client.factory.create('ns0:MXUserShowCurrencyCUS_Record')
		
		currencyRecord.id = ""
		currencyRecord.competition_id = 1
		currencyRecord.user_id = 1
		currencyRecord.piece = 200
		currencyRecord.buy_currency_value_id = 3
		currencyRecord.buy_date = config.NOW
		currencyRecord.buy_total = 2000
		currencyRecord.sell_currency_value_id = 3
		currencyRecord.sell_date = ""
		currencyRecord.sell_total = ""
		currencyRecord.status = ""
		currencyRecord.total = ""

		currency.MXUserShowCurrencyCUS_Record = currencyRecord
		currencyR.MXUserShowCurrencyCUS_Response = currency

		
		stockR = client.factory.create('ns0:MXUserShowStockCUS_ResponseR')
		stock = client.factory.create('ns0:MXUserShowStockCUS_Response')
		stockRecord = client.factory.create('ns0:MXUserShowStockCUS_Record')
		stockRecord.id = ""#id
		stockRecord.competition_id = ""#1
		stockRecord.user_id = ""#int(11)
		stockRecord.piece = ""#piece
		stockRecord.buy_stock_value_id = ""#value_id
		stockRecord.buy_date = config.NOW
		stockRecord.buy_total = ""#None
		stockRecord.sell_stock_value_id = ""#None
		stockRecord.sell_date = ""#None
		stockRecord.sell_total = ""#None
		stockRecord.status = ""#0
		stockRecord.total = ""#None
		stock.MXUserShowStockCUS_Record = stockRecord
		stockR.MXUserShowStockCUS_Response = stock
		result = client.service.MX_User_Manager_Currency_Stock_CUS_WSDLOperation("C", "true", "false", "", currencyR, stockR)
		print result
		#print result