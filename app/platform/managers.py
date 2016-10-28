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
		record = []
		if type == "S" and isCurrency:
			if not result.Currency.MXUserShowCurrencyCUS_Response == "":
				record = config.get_dict(result.Currency.MXUserShowCurrencyCUS_Response.MXUserShowCurrencyCUS_Record)
		else:
			if not result.Stock.MXUserShowStockCUS_Response == "":
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

	@staticmethod
	def order():
		#client = PlatformDataManager.get_instance().setup_client('/MX_User_Manager_Currency_Stock_Order_CUSWSDLService/MX_User_Manager_Currency_Stock_Order_CUSWSDLPort?wsdl')
		client = PlatformDataManager.get_instance().setup_client('%ssoap/platform/order/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)


		currency_buy = client.factory.create('ns1:MXUserShowCurrencyBuyOrder_Record')
		currency_buy.bank_id = 1
		currency_buy.buy_date = config.NOW
		currency_buy.competition_id = 1
		currency_buy.created_at = config.NOW
		currency_buy.currency_id = 1
		currency_buy.id = ""
		currency_buy.order_type = True
		currency_buy.piece = 2000
		currency_buy.price = 2000
		currency_buy.status = ""
		currency_buy.ttlive = config.NOW
		currency_buy.user_id = 11


		currency_sell = client.factory.create('ns1:MXUserShowCurrencySellOrder_Record')		
		currency_sell.created_at = config.NOW
		currency_sell.currency_buy_sell_id
		currency_sell.id = 1
		currency_sell.max = 3000
		currency_sell.min = 2000
		currency_sell.status = ""
		currency_sell.ttlive = config.NOW
		

		stock_buy = client.factory.create('ns0:MXUserShowStockBuyOrder_Record')
		stock_buy.buy_date = config.NOW
		stock_buy.competition_id = 1
		stock_buy.created_at = config.NOW
		stock_buy.id = ""
		stock_buy.order_type = True
		stock_buy.price = 2000
		stock_buy.status = ""
		stock_buy.stock_id = 1
		stock_buy.ttlive = config.NOW
		stock_buy.user_id = 11


		stock_sell = client.factory.create('ns0:MXUserShowStockSellOrder_Record')		
		stock_sell.competition_id = 1
		stock_sell.created_at = config.NOW
		stock_sell.id = 1
		stock_sell.max = 3000
		stock_sell.min = 2000
		stock_sell.status = ""
		stock_sell.stock_buy_sell_id
		stock_sell.user_id = 11

		#result = client.service.MX_User_Manager_Currency_Stock_Order_CUSWSDLOperation('S', True, True, currency_buy, currency_sell, stock_buy, stock_sell)
		print client