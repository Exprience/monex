# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import os
import hashlib
import base64


from django.conf import settings
from app.config.managers import BaseDataManager
from app.config import config
from models import Manager


class ManagerDataManager(BaseDataManager):
	__instance = None

	def __init__(self):
		pass

	@staticmethod
	def get_instance():
		if ManagerDataManager.__instance is None:
			ManagerDataManager.__instance = ManagerDataManager()
		return ManagerDataManager.__instance

	@staticmethod
	def register(email, password, news = "", research = "", lesson = "", competition_type = "", competition = "", currency = "", stock = "", bank = "", competition_approval = "", is_superuser = "0", is_active = True, is_create = "0", id = ""):
		client = ManagerDataManager.get_instance().setup_client('/MX_Admin_Create_ManagerWSDLService/MX_Admin_Create_ManagerWSDLPort?wsdl')
		result = client.service.MX_Admin_Create_ManagerWSDLOperation(email, hashlib.md5(password).hexdigest(), is_superuser, is_active, news, research, lesson, competition_type, competition, currency, stock, bank, competition_approval, is_create, id)
		if result.status == "true":
			user = Manager()
			if hasattr(result.manager_id, "value"):
				user.id = int(result.manager_id.value)
				user.pk = int(result.manager_id.value)
			else:
				user.id = int(result.manager_id)
				user.pk = int(result.manager_id)
			user.last_login = None
			user.password = hashlib.md5(password).hexdigest()
			return user
		else:
			return None

	@staticmethod
	def unique(value):
		client = ManagerDataManager.get_instance().setup_client('/MX_Check_Duplicate_Username_Email_HTTPService/MX_Check_Duplicate_Username_Email_HTTPPort?wsdl')
		result = client.service.MX_Check_Duplicate_Username_Email_HTTPOperation(False, value, False)
		return result

	@staticmethod
	def admins():
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/admin/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled = True)
		result = client.service.MX_Admin_Show_Manager_Lists_WSDLOperation('')
		if result.isSuccess:
			records = config.get_dict(result.ManagerLists.MXAdminSelectManagers_Response.MXAdminSelectManagers_Record)
			return records
		else:
			return None

	@staticmethod
	def login(username, password):
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/login/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
		result = client.service.MX_Manager_Check_Login_WSDLOperation(username, hashlib.md5(password).hexdigest(), config.NOW)
		manager = Manager()
		if result.isSuccess:
			manager.fill_manager(result.manager_info.MXCheckIfEmailAndPassIsGood_Response.MXCheckIfEmailAndPassIsGood_Record)
		else:
			return "false"
		return manager

	@staticmethod
	def apply_manager(email ,link, token):
		client = ManagerDataManager.get_instance().setup_client('/MX_ADMIN_Send_Validation_EmailService/MX_ADMIN_Send_Validation_EmailPort?wsdl')
		result = client.service.MX_ADMIN_Send_Validation_EmailOperation(email, link, token)
		
	@staticmethod
	def manager_info(id):
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/info/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled = True)
		result = client.service.MX_Admin_Show_Manager_Info_WSDLOperation(id)
		user = Manager()
		user.fill_manager(result.manager_info.MXAdminShowManagerInfo_Response.MXAdminShowManagerInfo_Record)
		return user

	@staticmethod
	def set_password(id, new_password, old_password = '', is_create = True):
		client = ManagerDataManager.get_instance().setup_client('/MX_Manager_Set_PasswordWSDLService/MX_Manager_Set_PasswordWSDLPort?wsdl')
		result = client.service.MX_Manager_Set_PasswordWSDLOperation(is_create, hashlib.md5(new_password).hexdigest(), hashlib.md5(old_password).hexdigest(), id)
		return result

	@staticmethod
	def category_create(category_name, id, type, wallet_val = "", is_create = True):
		client = ManagerDataManager.get_instance().setup_client('/MX_NewsCategoryCreateUpdateWSDLService/MX_NewsCategoryCreateUpdateWSDLPort?wsdl')
		result = client.service.MX_NewsCategoryCreateUpdateWSDLOperation(is_create, category_name, id, type, wallet_val)
		return result


	@staticmethod
	def category_delete(manager_id, category_id, category_type):
		client = ManagerDataManager.get_instance().setup_client('/MX_NewsResearchLessonCategoryDeleteWSDLService/MX_NewsResearchLessonCategoryDeleteWSDLPort?wsdl')
		result = client.service.MX_NewsResearchLessonCategoryDeleteWSDLOperation(manager_id, category_id, category_type)
		return result
		

	@staticmethod
	def show_category(*args):
		category_list = []
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/category/list/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled = True)
		result = client.service.MX_ShowNewsResearchLessonCategoryWSDLOperation(args[0], args[1])
		
		if args[1] == '1':
			category = result.news_category.MXSelectNewsCategoryForShow_Response.MXSelectNewsCategoryForShow_Record
		elif args[1] == '2':
			category = result.research_category.MXSelectResearchCategoryForShow_Response.MXSelectResearchCategoryForShow_Record
		elif args[1] == '3':
			category = result.lesson_category.MXSelectLessonCategoryForShow_Response.MXSelectLessonCategoryForShow_Record
		elif args[1] == '4':
			category = result.competition_category.MXSelectCompetitionCategoryForShow_Response.MXSelectCompetitionCategoryForShow_Record
		
		for i in category:
			context = (i.id.value, i.category.value)
			category_list.append(context)
		
		return category_list
		
	@staticmethod
	def individually(manager_id, type, id):
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/individually/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
		result = client.service.MXManagerShowNewsResearchLessonIndividuallyWSDLOperation(type, manager_id, id)
		if type is 'N':
			result = result.News.MXManagerSelectNewsIndividually_Response.MXManagerSelectNewsIndividually_Record
		if type is 'R':
			result = result.Research.MXManagerSelectResearchIndividually_Response.MXManagerSelectResearchIndividually_Record
		if type is 'L':
			result = result.Lesson.MXManagerSelectLessonIndividually_Response.MXManagerSelectLessonIndividually_Record
		if type is 'C':
			result = result.Competition.MXManagerSelectCompetitionIndividually_Response.MXManagerSelectCompetitionIndividually_Record
		return result

	@staticmethod
	def select(manager_id, type, value1 ="", value2 = "", value3 = "", value4 = ""):
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/select/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled = True)
		result = client.service.MXManagerShowNewsResearchLessonListsWSDLOperation(type, manager_id, value1, value2, value3, value4)
		records = None
		if type is 'N':
			if result.news_list.MXManagerShowNewsLists_Response:
				if manager_id is "":
					records = config.get_dict(result.news_list.MXManagerShowNewsLists_Response.MXUserShowNews_Record)
				else:
					records = config.get_dict(result.news_list.MXManagerShowNewsLists_Response.MXManagerShowNewsLists_Record)				

		elif type is 'R':
			if result.research_list.MXManagerShowResearchLists_Response:
				if manager_id is "":
					records = config.get_dict(result.research_list.MXManagerShowResearchLists_Response.MXUserShowResearchLists_Record)
				else:
					records = config.get_dict(result.research_list.MXManagerShowResearchLists_Response.MXManagerShowResearchLists_Record)
	
		elif type is 'L':
			if result.lesson_list.MXManagerShowLessonLists_Response:
				if manager_id is "":
					records = config.get_dict(result.lesson_list.MXManagerShowLessonLists_Response.MXUserShowLessonLists_Record)
				else:
					records = config.get_dict(result.lesson_list.MXManagerShowLessonLists_Response.MXManagerShowLessonLists_Record)
		
		elif type is 'C':
			if result.competition_list.MXManagerShowCompetitionLists_Response:
				if manager_id is "":
					records = config.get_dict(result.competition_list.MXManagerShowCompetitionLists_Response.MXUserShowCompetitionLists_Record)
				else:
					records = config.get_dict(result.competition_list.MXManagerShowCompetitionLists_Response.MXManagerShowCompetitionLists_Record)

		return records

	@staticmethod
	def create(type, created_by, category, body = "", title = "", author_email = "", author_name = "", url = "", fee = "", prize="", start_date = config.NOW , end_date = config.NOW, register_low = "", status="", file = ""):
		client = ManagerDataManager.get_instance().setup_client('/MX_Insert_Into_News_Research_LessonService/MX_Insert_Into_News_Research_LessonPort?wsdl')
		
		news = client.factory.create('ns1:NewsRecord')
		news.created_by = created_by
		news.created_at = config.NOW
		news.category = category
		news.title = title
		news.body = body

		research = client.factory.create('ns1:ResearchRecord')
		research.created_by = created_by
		research.created_at = config.NOW
		try:
			with open(file.path, "rb") as f:
				data = f.read()
				research.pdf_file = base64.b64encode(data)
			research.file_type = os.path.splitext(file.path)[1]
		except:
			research.pdf_file = file
			research.file_type = ""
		research.author_name = author_name
		research.title = title
		research.research_category_id = category
		research.author_email = author_email

		lesson = client.factory.create('ns1:LessonRecord')
		lesson.created_by = created_by
		lesson.created_at = config.NOW
		lesson.author_email = author_email
		lesson.author_name = author_name
		lesson.url = url
		lesson.title = title
		lesson.lesson_category_id = category

		competition = client.factory.create('ns1:CompetitionRecord')
		competition.status = status
		competition.register_low = register_low
		competition.created_by = created_by
		competition.created_at = config.NOW
		competition.end_date = end_date
		competition.start_date = start_date
		competition.prize = prize
		competition.fee = fee
		competition.competition_category_id = category

		result = client.service.MX_Insert_Into_News_Research_LessonOperation(type, news, research, lesson, competition, created_by)
		return result

	@staticmethod
	def update(type, manager_id, id, category, title = "", body = "", url = "", author_name = "", author_email = "", fee = "", prize="", start_date = config.NOW , end_date = config.NOW, register_low = "", file = None):
		client = ManagerDataManager.get_instance().setup_client('/MX_Manager_Update_News_Research_LessonService/MX_Manager_Update_News_Research_LessonPort?wsdl')
		
		news = client.factory.create('ns0:News')
		news.MXManagerUpdateNews_Request.id = id
		news.MXManagerUpdateNews_Request.category = category
		news.MXManagerUpdateNews_Request.title = title
		news.MXManagerUpdateNews_Request.body = body
		
		research = client.factory.create('ns0:Research')
		research.MXManagerUpdateResearch_Request.research_category_id = category
		research.MXManagerUpdateResearch_Request.title = title
		research.MXManagerUpdateResearch_Request.author_name = author_name
		research.MXManagerUpdateResearch_Request.author_email = author_email
		try:
			with open(file.path, "rb") as f:
				data = f.read()
				research.MXManagerUpdateResearch_Request.pdf_file = base64.b64encode(data)
			research.MXManagerUpdateResearch_Request.file_type = os.path.splitext(file.path)[1]
		except:
			pass
		research.MXManagerUpdateResearch_Request.id = id

		lesson = client.factory.create('ns0:Lesson')
		lesson.MXManagerUpdateLesson_Request.lesson_category_id = category
		lesson.MXManagerUpdateLesson_Request.title = title
		lesson.MXManagerUpdateLesson_Request.url = url
		lesson.MXManagerUpdateLesson_Request.author_name = author_name
		lesson.MXManagerUpdateLesson_Request.author_email = author_email
		lesson.MXManagerUpdateLesson_Request.id = id
		
		competition = client.factory.create('ns0:Competition')
		competition.MXManagerUpdateCompetition_Request.competition_category_id = category
		competition.MXManagerUpdateCompetition_Request.fee = fee
		competition.MXManagerUpdateCompetition_Request.prize = prize
		competition.MXManagerUpdateCompetition_Request.start_date = start_date
		competition.MXManagerUpdateCompetition_Request.end_date = end_date
		competition.MXManagerUpdateCompetition_Request.register_low = register_low
		competition.MXManagerUpdateCompetition_Request.id = id

		result = client.service.MX_Manager_Update_News_Research_LessonOperation(type, manager_id, news, research, lesson, competition)
		return result

	@staticmethod
	def delete(type, manager_id, id):
		client = ManagerDataManager.get_instance().setup_client('/MX_Manager_Delete_News_Lesson_ResearchWSDLService/MX_Manager_Delete_News_Lesson_ResearchWSDLPort?wsdl')
		result = client.service.MX_Manager_Delete_News_Lesson_ResearchWSDLOperation(type, manager_id, id)
		return result

	@staticmethod
	def get_manager(value, isId = True):
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/get/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
		result = client.service.MX_ManagerGetIdLastLoginCredentialsWSDLOperation(value, isId)
		user = Manager()
		if isId:
			user.pk = result.Credentials.MXManagerSelectCredentials_Response.MXManagerSelectCredentials_Record.id.value
			user.fill_manager(result.Credentials.MXManagerSelectCredentials_Response.MXManagerSelectCredentials_Record)
		else:
			if result.Credentials.MXManagerSelectCredentials_Response:
				user.pk = result.Credentials.MXManagerSelectCredentials_Response.MXManagerSelectCredentialsByEmail_Record.id.value
				user.fill_manager(result.Credentials.MXManagerSelectCredentials_Response.MXManagerSelectCredentialsByEmail_Record)
		return user

	@staticmethod
	def bank(manager_id, type, id = 0, name = "", short_name = "", icon = ""):
		lists = []
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/bank/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
		
		bank = client.factory.create('ns0:MXManagerUpdateToBank_RequestR')
		request = client.factory.create('ns:MXManagerUpdateToBank_Request')
		request.id = id
		request.name = name
		request.short_name = short_name
		request.icon = icon
		bank.MXManagerUpdateToBank_Request = request

		result = client.service.MX_Manager_CUDS_BankWSDLOperation(manager_id, type, bank)
		if type == "S":
			if result.isSuccess == "true":
				for i in result.bankList.MXManagerSelectAll_Response.MXManagerSelectAll_Record:
					context = {}
					context['id'] = unicode(i.id.value)
					if i.name._isNull == "false":
						context['name'] = unicode(i.name.value)
					else:
						context['name'] = texts.NULL_TEXT
					if i.short_name._isNull == "false":
						context['short_name'] = unicode(i.short_name.value)
					else:
						context['short_name'] = texts.NULL_TEXT
					if i.icon._isNull == "false":
						context['icon'] = unicode(i.icon.value)
					else:
						context['icon'] = texts.NULL_TEXT
					lists.append(context)
			return lists
		else:
			return result

	@staticmethod
	def currency(manager_id, type, id = 0, name = "", short_name = "", icon = "", symbol = ""):
		lists = []
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/currency/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
		
		currency = client.factory.create('ns:MXManagerUpdateToCurrency_RequestR')
		request = client.factory.create('ns:MXManagerUpdateToCurrency_Request')
		request.id = id
		request.name = name
		request.short_name = short_name
		request.icon = icon
		request.symbol = symbol
		currency.MXManagerUpdateToCurrency_Request = request

		result = client.service.MX_Manager_CUDS_CurrencyWSDLOperation(manager_id, type, currency)
		if type == "S":
			if result.isSuccess == "true":
				for i in result.currencyList.MXManagerCurrencySelectAll_Response.MXManagerCurrencySelectAll_Record:
					context = {}
					context['id'] = i.id.value
					if i.name._isNull == "false":
						context['name'] = i.name.value
					else:
						context['name'] = texts.NULL_TEXT
					if i.short_name._isNull == "false":
						context['short_name'] = i.short_name.value
					else:
						context['short_name'] = texts.NULL_TEXT
					if i.symbol._isNull == "false":
						context['symbol'] = i.symbol.value
					else:
						context['symbol'] = texts.NULL_TEXT
					if i.icon._isNull == "false":
						context['icon'] = i.icon.value
					else:
						context['icon'] = texts.NULL_TEXT
					lists.append(context)
			return lists
		else:
			return result

	@staticmethod
	def stock(manager_id, type, id = 0, name = "", symbol = ""):
		lists = []
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/stock/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
		
		currency = client.factory.create('ns:MXManagerUpdateToStock_RequestR')
		request = client.factory.create('ns:MXManagerUpdateToStock_Request')
		request.id = id
		request.name = name
		request.symbol = symbol
		currency.MXManagerUpdateToStock_Request = request

		result = client.service.MX_Manager_CUDS_StockWSDLOperation(manager_id, type, currency)
		if type == "S":
			if result.isSuccess == "true":
				records = result.stockList.MXManagerSelectAllStock_Response.MXManagerSelectAllStock_Record
				if hasattr(records, 'id'):
					context = {}
					context['id'] = records.id.value
					if records.name._isNull == "false":
						context['name'] = records.name.value
					else:
						context['name'] = texts.NULL_TEXT
					if records.symbol._isNull == "false":
						context['symbol'] = records.symbol.value
					else:
						context['symbol'] = texts.NULL_TEXT
					lists.append(context)
				else:
					for i in records:
						context = {}
						context['id'] = i.id.value
						if i.name._isNull == "false":
							context['name'] = i.name.value
						else:
							context['name'] = texts.NULL_TEXT
						if i.symbol._isNull == "false":
							context['symbol'] = i.symbol.value
						else:
							context['symbol'] = texts.NULL_TEXT
						lists.append(context)
			return lists
		else:
			return result

	@staticmethod
	def currency_create(manager_id, bank, currency, buy, sell):
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/currency/create.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
		currency_value = client.factory.create('ns:MXManagerInsertIntoCurrencyValue_RequestR')
		request = client.factory.create('ns0:MXManagerInsertIntoCurrencyValue_Request')
		request.bank_id = bank
		request.currency_id = currency
		request.buy = buy
		request.sell = sell
		request.created_at = config.NOW
		request.created_by = manager_id
		currency_value.MXManagerInsertIntoCurrencyValue_Request = request
		result = client.service.MX_Manager_Add_Currency_ValueOperation(manager_id, currency_value)
		return result

	@staticmethod
	def stock_create(manager_id, stock, open, buy, sell, high, low, last, close, now):
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/stock/create.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
		stock = client.factory.create('ns:MXManagerInsertIntoStockValue_RequestR')
		request = client.factory.create('ns:MXManagerInsertIntoStockValue_Request')
		request.stock_id = stock
		request.open = open
		request.buy = buy
		request.sell = sell
		request.high = high
		request.low = low
		request.last = last
		request.close = close
		request.created_at = config.NOW
		request.created_by = manager_id
		stock.MXManagerInsertIntoStockValue_Request = request
		result = client.service.MX_Manager_Add_Stock_ValueWSDLOperation(stock)
		return result

	@staticmethod
	def list(type, start_date, end_date, id = "", is_currency = True):
		client = ManagerDataManager.get_instance().setup_client('%ssoap/manager/list.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled=True)
		result = client.service.MX_Manager_User_Show_Currency_Stock_Value_WSDLOperation(type, id, start_date, end_date, is_currency)
		if result.isSuccess:
			if type == "L":
				if is_currency:
					records = config.get_dict(result.Currency.MXManagerUserShowCurrency_Response.MXManagerUserShowCurrencyLast_Record)
				else:
					records = config.get_dict(result.Stock.MXManagerUserShowStock_Response.MXManagerUserShowStockLast_Record)
			elif type == "I":
				if is_currency:
					records = config.get_dict(result.Currency.MXManagerUserShowCurrency_Response.MXManagerUserShowCurrencyIndividually_Record)
				else:
					records = config.get_dict(result.Stock.MXManagerUserShowStock_Response.MXManagerUserShowStockIndividually_Record)
			else:
				if is_currency:
					records = config.get_dict(result.Currency.MXManagerUserShowCurrency_Response.MXManagerUserShowCurrency_Record)
				else:
					records = config.get_dict(result.Stock.MXManagerUserShowStock_Response.MXManagerUserShowStock_Record)
			return records
		else:
			return None
