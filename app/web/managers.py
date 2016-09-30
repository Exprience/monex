# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import base64

from django.conf import settings
from app.config.managers import BaseDataManager
from app.config import status, config


class WebBaseDataManager(BaseDataManager):


	@staticmethod
	def register(types, id = "", manager_id = "", competition_id = "", user_id = "", file="", is_approved = False, is_manager = False):
		try:
			client = WebBaseDataManager.get_instance().setup_client('%ssoap/web/competition/soap.wsdl' % settings.STATIC_DOMAIN_URL, serverAddressFilled = True)
			register = client.factory.create("ns:competition_registerR")
			request = client.factory.create("ns:competition_register")
			request.id = id
			request.competition_id = competition_id
			request.user_id = user_id
			try:
				print 1/0
				with open(file.path, "rb") as f:
					data = f.read()
					request.file = base64.b64encode(data)
			except Exception, e:
				pass
			request.status = status.CR_NOT_APPROVED
			request.created_at = config.NOW
			register.competition_register = request
			result = client.service.MX_User_Manager_Competition_Register_CUS_WSDLOperation(is_manager, types, register, manager_id, is_approved)
			if result.Response == 3:
				return ""
			else:
				if types == "S":
					if is_manager:
						record = config.get_dict(result.competitionRegisterResponse.MXManagerSelectCompReg_Response.MXManagerSelectCompReg_Record)
					else:
						record = config.get_dict(result.competitionRegisterResponse.MXManagerSelectCompReg_Response.MXUserSelectCompReg_Record)
					return record
				elif types == "U":
					return result
			return result
		except:
			return config.SYSTEM_ERROR

	@staticmethod
	def if_register(competition_id, user_id):
		try:
			client = WebBaseDataManager.get_instance().setup_client('/MX_SYSTEM_Check_Is_Registered_In_CompetitionWSDLService/MX_SYSTEM_Check_Is_Registered_In_CompetitionWSDLPort?wsdl')
			result = client.service.MX_SYSTEM_Check_Is_Registered_In_CompetitionWSDLOperation(user_id, competition_id)
			return result
		except:
			return None