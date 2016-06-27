from datetime import date, timedelta, datetime
from django.utils.http import urlsafe_base64_encode as e, urlsafe_base64_decode as d, base36_to_int
from django.utils.encoding import force_bytes as f


class CompetitionRegisterToken(object):


	def encode(self, user_id, competition_id, register_id, register_time):
		token_list = []
		token_list.append(e( f(user_id) ))
		token_list.append(e( f( competition_id ) ))
		token_list.append(e( f( register_id ) ))
		token_list.append(e( f( ( register_time.date() - date(2001, 1, 1)).days)))
		print type(register_time.date() - date(2001, 1, 1))
		return ('-'.join(i for i in token_list))

	def decode(self, value):
		try:
			c_user_id ,c_competition_id, c_register_id, c_register_time = value.split('-')
			c_register_time = date(2001, 1, 1) + timedelta(int(d(c_register_time)))
			return {
				'user_id': int(d(c_user_id)) ,
				'competition_id': int(d(c_competition_id)),
				'register_id':  int(d(c_register_id)),
				'registered_date':  c_register_time
				}
		except ValueError:
			return False
	
	def check_token(self, user_id, value):
		'''competition_id, register_id, register_time,'''
		try:
			c_user_id ,c_competition_id, c_register_id, c_register_time = value.split('-')
		except ValueError:
			return False
		
		if f(user_id) != d(c_user_id):
			print f(user_id)
			print d(c_user_id)
			return False
		
		#if f(competition_id) != d(c_competition_id):
		#	return False
		
		#if f(register_id) != d(c_register_id):
		#	return False
		
		#if f((register_time.date() - date(2001, 1, 1)).days) != d(c_register_time):
		#	return False

		return True

competition_register_token = CompetitionRegisterToken()