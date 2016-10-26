# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from datetime import datetime, timedelta


from app.config.managers import BaseDataManager
from django.conf import settings
from app.config import config

class PlatformDataManager(BaseDataManager):

	__instance = None

	def __init__(self):
		pass

	@staticmethod
	def get_instance():
		if PlatformDataManager.__instance is None:
			PlatformDataManager.__instance = PlatformDataManager()
		return PlatformDataManager.__instance

	
	@staticmethod
	def currency(type, competition_id, user_id, piece = 1, value_id = 1, id = 1, isCurrency = True, isManager = False, manager_id = ""):
		client = PlatformDataManager.get_instance().setup_client('%ssoap/platform/buy_sell/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
		
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
			if result.Currency.MXUserShowCurrencyCUS_Response == "":
				record = []
			else:
				record = config.get_dict(result.Currency.MXUserShowCurrencyCUS_Response.MXUserShowCurrencyCUS_Record)
		else:
			if result.Stock.MXUserShowStockCUS_Response == "":
				record = []
			else:
				record = config.get_dict(result.Stock.MXUserShowStockCUS_Response.MXUserShowStockCUS_Record)
		if type == "C":
			return result
		return record

	@staticmethod
	def alert(type, user_id, competition_id, isBuy = 1, isHigherThan = 1, price = 0, id = 0):
		client = PlatformDataManager.get_instance().setup_client('%ssoap/platform/alert/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
		alert = client.factory.create('ns0:MXUserSelectPriceAlert_RecordR')
		alert_record = client.factory.create('ns0:MXUserSelectPriceAlert_Record')
		
		alert_record.id = int(id)
		alert_record.user_id = int(user_id)
		alert_record.competition_id = int(competition_id)
		alert_record.isCurrency = 1
		alert_record.isBuy = isBuy
		alert_record.isHigherThan = isHigherThan
		alert_record.price = int(price)
		alert_record.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		alert_record.de_day = (datetime.now() + timedelta(90)).strftime("%Y-%m-%d %H:%M:%S")
		alert_record.status = ""
		alert.MXUserSelectPriceAlert_Record = alert_record
		

		result = client.service.MX_User_Price_Alert_CUDSWSDLOperation(type, alert)
		if type == "S":
			record = config.get_dict(result.priceAlert.MXUserSelectPriceAlert_Response.MXUserSelectPriceAlert_Record)
			return record
		return result