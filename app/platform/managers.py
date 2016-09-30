# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from app.config.managers import BaseDataManager
from django.conf import settings
from app.config import config

class PlatformBaseDataManager(BaseDataManager):
	
	@staticmethod
	def currency(type, competition_id, user_id, piece = 1, value_id = 1, id = 1, isCurrency = True, isManager = False, manager_id = ""):
		#try:
			client = PlatformBaseDataManager.get_instance().setup_client('%ssoap/platform/buy_sell/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
			
			currencyR = client.factory.create('ns0:MXUserShowCurrencyCUS_ResponseR')
			currency = client.factory.create('ns0:MXUserShowCurrencyCUS_Response')
			currencyRecord = client.factory.create('ns0:MXUserShowCurrencyCUS_Record')
			
			currencyRecord.id = id
			currencyRecord.competition_id = competition_id
			currencyRecord.user_id = user_id
			currencyRecord.piece = piece
			currencyRecord.buy_currency_value_id = value_id
			currencyRecord.buy_date = config.NOW
			currencyRecord.buy_total = 200
			currencyRecord.sell_currency_value_id = value_id
			currencyRecord.sell_date = config.NOW
			currencyRecord.sell_total = 200
			currencyRecord.status = 1
			currencyRecord.total = 200

			currency.MXUserShowCurrencyCUS_Record = currencyRecord
			currencyR.MXUserShowCurrencyCUS_Response = currency

			
			stockR = client.factory.create('ns0:MXUserShowStockCUS_ResponseR')
			stock = client.factory.create('ns0:MXUserShowStockCUS_Response')
			stockRecord = client.factory.create('ns0:MXUserShowStockCUS_Record')
			stockRecord.id = id
			stockRecord.competition_id = competition_id
			stockRecord.user_id = user_id
			stockRecord.piece = piece
			stockRecord.buy_stock_value_id = value_id
			stockRecord.buy_date = config.NOW
			stockRecord.buy_total = 200
			stockRecord.sell_stock_value_id = value_id
			stockRecord.sell_date = config.NOW
			stockRecord.sell_total = 200
			stockRecord.status = 1
			stockRecord.total = 200
			stock.MXUserShowStockCUS_Record = stockRecord
			stockR.MXUserShowStockCUS_Response = stock
			result = client.service.MX_User_Manager_Currency_Stock_CUS_WSDLOperation(type, isCurrency, isManager, manager_id, currencyR, stockR)
			if type == "S" and isCurrency:
				record = config.get_dict(result.Currency.MXUserShowCurrencyCUS_Response.MXUserShowCurrencyCUS_Record)
			else:
				record = config.get_dict(result.Stock.MXUserShowStockCUS_Response.MXUserShowStockCUS_Record)
			return record
		#except:
		#	return config.SYSTEM_ERROR