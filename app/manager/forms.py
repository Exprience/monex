# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django import forms
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from managers import ManagerDataManager as manager
from app.config import config

from redactor.widgets import RedactorEditor
from django.utils.safestring import mark_safe

from widget import PopUpWidget
from bootstrap3_datetime.widgets import DateTimePicker


class LoginForm(forms.Form):
	email = forms.EmailField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'И-мэйл'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':'Нууц үг'}))
	remember_me = forms.BooleanField(required = False, initial = True, label = 'Намайг сана')

	def clean_remember_me(self):
		remember_me = self.cleaned_data['remember_me']
		if not remember_me:
			settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
		else:
			settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
		return remember_me


class ManagerForm(forms.Form):

	email = forms.EmailField(label = u'И-мэйл', widget = forms.TextInput(attrs = {'class':'form-control'}))

	is_active = forms.BooleanField(label = 'Хандах эрх', required = False)
	
	news_create = forms.BooleanField(required = False)
	news_update = forms.BooleanField(required = False)
	news_delete = forms.BooleanField(required = False)

	research_create = forms.BooleanField(required = False)
	research_update = forms.BooleanField(required = False)
	research_delete = forms.BooleanField(required = False)

	lesson_create = forms.BooleanField(required = False)
	lesson_update = forms.BooleanField(required = False)
	lesson_delete = forms.BooleanField(required = False)

	competition_type_create = forms.BooleanField(required = False)
	competition_type_update = forms.BooleanField(required = False)
	competition_type_delete = forms.BooleanField(required = False)

	competition_create = forms.BooleanField(required = False)
	competition_update = forms.BooleanField(required = False)
	competition_delete = forms.BooleanField(required = False)

	competition_approval_create = forms.BooleanField(required = False)
	competition_approval_update = forms.BooleanField(required = False)
	competition_approval_delete = forms.BooleanField(required = False)

	
	stock_create = forms.BooleanField(required = False)
	stock_update = forms.BooleanField(required = False)
	stock_delete = forms.BooleanField(required = False)

	currency_create = forms.BooleanField(required = False)
	currency_update = forms.BooleanField(required = False)
	currency_delete = forms.BooleanField(required = False)

	bank_create = forms.BooleanField(required = False)
	bank_update = forms.BooleanField(required = False)
	bank_delete = forms.BooleanField(required = False)
	
	def __init__(self, id = None, info = False, *args, **kwargs):
		super(ManagerForm, self).__init__(*args, **kwargs)
		if info:
			self.fields['email'].widget.attrs['disabled'] = 'disabled'
			self.fields['news_create'].widget.attrs['disabled'] = 'disabled'
			self.fields['news_update'].widget.attrs['disabled'] = 'disabled'
			self.fields['news_delete'].widget.attrs['disabled'] = 'disabled'
			self.fields['research_create'].widget.attrs['disabled'] = 'disabled'
			self.fields['research_update'].widget.attrs['disabled'] = 'disabled'
			self.fields['research_delete'].widget.attrs['disabled'] = 'disabled'
			self.fields['lesson_create'].widget.attrs['disabled'] = 'disabled'
			self.fields['lesson_update'].widget.attrs['disabled'] = 'disabled'
			self.fields['lesson_delete'].widget.attrs['disabled'] = 'disabled'
			self.fields['competition_type_create'].widget.attrs['disabled'] = 'disabled'
			self.fields['competition_type_update'].widget.attrs['disabled'] = 'disabled'
			self.fields['competition_type_delete'].widget.attrs['disabled'] = 'disabled'
			self.fields['competition_create'].widget.attrs['disabled'] = 'disabled'
			self.fields['competition_update'].widget.attrs['disabled'] = 'disabled'
			self.fields['competition_delete'].widget.attrs['disabled'] = 'disabled'
			self.fields['stock_create'].widget.attrs['disabled'] = 'disabled'
			self.fields['stock_update'].widget.attrs['disabled'] = 'disabled'
			self.fields['stock_delete'].widget.attrs['disabled'] = 'disabled'
			self.fields['currency_create'].widget.attrs['disabled'] = 'disabled'
			self.fields['currency_update'].widget.attrs['disabled'] = 'disabled'
			self.fields['currency_delete'].widget.attrs['disabled'] = 'disabled'
			self.fields['bank_create'].widget.attrs['disabled'] = 'disabled'
			self.fields['bank_update'].widget.attrs['disabled'] = 'disabled'
			self.fields['bank_delete'].widget.attrs['disabled'] = 'disabled'
			self.fields['competition_approval_create'].widget.attrs['disabled'] = 'disabled'
			self.fields['competition_approval_update'].widget.attrs['disabled'] = 'disabled'
			self.fields['competition_approval_delete'].widget.attrs['disabled'] = 'disabled'
			self.fields['is_active'].widget.attrs['disabled'] = 'disabled'
		if id:
			try:
				self.id = id
				user = manager.manager_info(id)
				self.fields['email'].widget.attrs['disabled'] = 'disabled'
				self.fields['email'].initial = user.email
				self.fields['email'].required = False
				if user.is_active == '1':
					self.fields['is_active'].initial = True

				if config.convert_10_2(user.news)[0] == '1':
					self.fields['news_create'].initial = True

				if config.convert_10_2(user.news)[1] == '1':
					self.fields['news_update'].initial = True

				if config.convert_10_2(user.news)[2] == '1':
					self.fields['news_delete'].initial = True

				if config.convert_10_2(user.research)[0] == '1':
					self.fields['research_create'].initial = True

				if config.convert_10_2(user.research)[1] == '1':
					self.fields['research_update'].initial = True

				if config.convert_10_2(user.research)[2] == '1':
					self.fields['research_delete'].initial = True

				if config.convert_10_2(user.lesson)[0] == '1':
					self.fields['lesson_create'].initial = True

				if config.convert_10_2(user.lesson)[1] == '1':
					self.fields['lesson_update'].initial = True

				if config.convert_10_2(user.lesson)[2] == '1':
					self.fields['lesson_delete'].initial = True

				if config.convert_10_2(user.competition_type)[0] == '1':
					self.fields['competition_type_create'].initial = True

				if config.convert_10_2(user.competition_type)[1] == '1':
					self.fields['competition_type_update'].initial = True

				if config.convert_10_2(user.competition_type)[2] == '1':
					self.fields['competition_type_delete'].initial = True

				if config.convert_10_2(user.competition)[0] == '1':
					self.fields['competition_create'].initial = True

				if config.convert_10_2(user.competition)[1] == '1':
					self.fields['competition_update'].initial = True

				if config.convert_10_2(user.competition)[2] == '1':
					self.fields['competition_delete'].initial = True

				if config.convert_10_2(user.competition_approval)[0] == '1':
					self.fields['competition_approval_create'].initial = True

				if config.convert_10_2(user.competition_approval)[1] == '1':
					self.fields['competition_approval_update'].initial = True

				if config.convert_10_2(user.competition_approval)[2] == '1':
					self.fields['competition_approval_delete'].initial = True

				if config.convert_10_2(user.stock)[0] == '1':
					self.fields['stock_create'].initial = True

				if config.convert_10_2(user.stock)[1] == '1':
					self.fields['stock_update'].initial = True

				if config.convert_10_2(user.stock)[2] == '1':
					self.fields['stock_delete'].initial = True

				if config.convert_10_2(user.bank)[0] == '1':
					self.fields['bank_create'].initial = True

				if config.convert_10_2(user.bank)[1] == '1':
					self.fields['bank_update'].initial = True

				if config.convert_10_2(user.bank)[2] == '1':
					self.fields['bank_delete'].initial = True

				if config.convert_10_2(user.currency)[0] == '1':
					self.fields['currency_create'].initial = True

				if config.convert_10_2(user.currency)[1] == '1':
					self.fields['currency_update'].initial = True

				if config.convert_10_2(user.currency)[2] == '1':
					self.fields['currency_delete'].initial = True
			except:
				pass

	def clean_email(self):
		email = self.cleaned_data['email']
		status = manager.unique(email)
		if not status:
			raise forms.ValidationError(u'И-мэйл хаяг бүртгэлтэй байна', code='invalid')
		return email

	def save(self, request):
		news = config.convert_2_10(int(self.cleaned_data['news_create']), int(self.cleaned_data['news_update']), int(self.cleaned_data['news_delete']))
		research = config.convert_2_10(int(self.cleaned_data['research_create']), int(self.cleaned_data['research_update']), int(self.cleaned_data['research_delete']))
		lesson = config.convert_2_10(int(self.cleaned_data['lesson_create']), int(self.cleaned_data['lesson_update']), int(self.cleaned_data['lesson_delete']))
		competition_type = config.convert_2_10(int(self.cleaned_data['competition_type_create']), int(self.cleaned_data['competition_type_update']), int(self.cleaned_data['competition_type_delete']))
		competition = config.convert_2_10(int(self.cleaned_data['competition_create']), int(self.cleaned_data['competition_update']), int(self.cleaned_data['competition_delete']))
		competition_approval = config.convert_2_10(int(self.cleaned_data['competition_approval_create']), int(self.cleaned_data['competition_approval_update']), int(self.cleaned_data['competition_approval_delete']))
		stock = config.convert_2_10(int(self.cleaned_data['stock_create']), int(self.cleaned_data['stock_update']), int(self.cleaned_data['stock_delete']))
		currency = config.convert_2_10(int(self.cleaned_data['currency_create']), int(self.cleaned_data['currency_update']), int(self.cleaned_data['currency_delete']))
		bank = config.convert_2_10(int(self.cleaned_data['bank_create']), int(self.cleaned_data['bank_update']), int(self.cleaned_data['bank_delete']))
		
		
		if not hasattr(self, 'id'):
			result = manager.register(self.cleaned_data['email'], config.password(), news = news, research = research, lesson = lesson, competition_type = competition_type, competition = competition, currency = currency, stock = stock, bank = bank, competition_approval = competition_approval, is_create = True, is_active = self.cleaned_data['is_active'])
			if result:
				current_site = get_current_site(request)
				site_name = current_site.name
				domain = current_site.domain
				uid = urlsafe_base64_encode(force_bytes(result.pk))
				token = default_token_generator.make_token(result)
				link = 'http://%s/manager/reset/%s/%s/' %(domain, uid, token)
				manager.apply_manager("uuganbat@innosol.mn", link, token)
		else:
			result = manager.register("", "", news = news, research = research, lesson = lesson, competition_type = competition_type, competition = competition, currency = currency, stock = stock, bank = bank, competition_approval = competition_approval, is_create = False, id = self.id, is_active = self.cleaned_data['is_active'])
		return result


class ManagerSetPasswordForm(forms.Form):
	new_password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':'Нууц үг'}))
	new_password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':'Нууц үг давтах'}))


	def clean(self):
		cleaned_data = super(ManagerSetPasswordForm, self).clean()
		if self.is_valid():
			if cleaned_data['new_password1'] != cleaned_data['new_password2']:
				raise forms.ValidationError(u'Нууц үг таарахгүй байна', code = 'invalid')
		return cleaned_data

	def save(self, user):
		result = manager.set_password(user.id, self.cleaned_data['new_password1'])
		return result


class CategoryForm(forms.Form):
	category = forms.CharField(label = u'Ангилал', widget = forms.TextInput(attrs = {'class':'form-control'}))

	def __init__(self, id = None, type = None, delete_id = None, *args, **kwargs):
		super(CategoryForm, self).__init__(*args, **kwargs)
		if delete_id:
			self.fields['category'].disabled = True
			self.fields['category'].initial = delete_id


class CompetitionCategoryForm(forms.Form):
	category = forms.CharField(label = u'Ангилал', widget = forms.TextInput(attrs = {'class':'form-control'}))
	wallet_val = forms.IntegerField(label = u'Түрийвч', widget = forms.TextInput(attrs = {'class':'form-control'}))

	def __init__(self, id = None, delete_id = None, *args, **kwargs):
		super(CompetitionCategoryForm, self).__init__(*args, **kwargs)
		if delete_id:
			self.fields['category'].disabled = True
			self.fields['category'].initial = delete_id


class NewsForm(forms.Form):
	category = forms.ChoiceField()
	title = forms.CharField(label = u'Гарчиг', widget = forms.TextInput(attrs = {'class':'form-control'}))
	body = forms.CharField(label = u'Мэдээ',widget = RedactorEditor(attrs = {'class':'form-control'}))
	

	def __init__(self, manager_id = None, type = None, id = None, is_delete = False, *args, **kwargs):
		super(NewsForm, self).__init__(*args, **kwargs)
		self.fields['category'] = forms.ChoiceField(label = u'Ангилал', choices = tuple(manager.show_category(manager_id, type)), widget = forms.Select(attrs = {'class':'form-control', 'style':'width:90%'}))
		widget = self.fields['category'].widget
		if not is_delete:
			self.fields['category'].widget = PopUpWidget(widget, 'news', can_add_related = True, can_change_related = True, can_delete_related = True)
		if id:
			result = manager.individually(manager_id, 'N', id)
			self.fields['category'].initial = result.category.value
			self.fields['title'].initial = result.title.value
			self.fields['body'].initial = mark_safe(result.body.value)

		if is_delete:
			self.fields['category'].disabled = True
			self.fields['category'].widget.attrs = {'class':'form-control'}
			self.fields['title'].disabled = True
			self.fields['body'].disabled = True


class ResearchForm(forms.Form):
	category = forms.ChoiceField()
	title = forms.CharField(label = u'Гарчиг',widget = forms.TextInput(attrs = {'class':'form-control'}))
	file = forms.FileField(label = u'Pdf file',widget = forms.FileInput(attrs = {'class':'form-control'}))
	author_name = forms.CharField(label = u'Сургалт хийсэн багшийн нэр',widget = forms.TextInput(attrs = {'class':'form-control'}))
	author_email = forms.EmailField(label = u'Сургалт хийсэн багшийн и-мэйл',widget = forms.TextInput(attrs = {'class':'form-control'}))

	def __init__(self, id = None, manager_id = None, type = None, is_delete = None, *args, **kwargs):
		super(ResearchForm, self).__init__(*args, **kwargs)
		self.fields['category'] = forms.ChoiceField(label = u'Ангилал', choices = tuple(manager.show_category(manager_id, type)), widget = forms.Select(attrs = {'class':'form-control', 'style':'width:90%'}))
		widget = self.fields['category'].widget
		if not is_delete:
			self.fields['category'].widget = PopUpWidget(widget, 'research', can_add_related = True, can_change_related = True, can_delete_related = True)
		if id:
			result = manager.individually(manager_id, "R", id)
			self.fields['category'].initial = result.research_category_id.value
			self.fields['title'].initial = result.title.value
			self.fields['file'].initial = result.pdf_file.value
			self.fields['author_name'].initial = result.author_name.value
			if hasattr(result.author_email, 'value'):
				self.fields['author_email'].initial = result.author_email.value

class CompetitionForm(forms.Form):
	category = forms.ChoiceField()
	fee = forms.IntegerField(label = u'Бүртгэлийн хураамж', widget = forms.TextInput(attrs = {'class':'form-control'}))
	prize = forms.IntegerField(label = u'Эхлэх данс', widget = forms.TextInput(attrs = {'class':'form-control'}))
	start_date = forms.CharField(label = u'Эхлэх өдөр', widget = DateTimePicker(attrs = {'class':'form-control'}, options={"format": "YYYY-MM-DD HH:mm", "pickSeconds": False}))
	end_date = forms.CharField(label = u'Дуусах өдөр', widget = DateTimePicker(attrs = {'class':'form-control'}, options={"format": "YYYY-MM-DD HH:mm", "pickSeconds": False}))
	register_low = forms.IntegerField(label = u'Бүртгэлийн доод хязгаар', widget = forms.TextInput(attrs = {'class':'form-control'}))

	def __init__(self, manager_id = None, type = None, id = None,*args, **kwargs):
		super(CompetitionForm, self).__init__(*args, **kwargs)
		self.fields['category'] = forms.ChoiceField(label = u'Ангилал', choices = tuple(manager.show_category(manager_id, type)), widget = forms.Select(attrs = {'class':'form-control', 'style':'width:90%'}))
		widget = self.fields['category'].widget
		self.fields['category'].widget = PopUpWidget(widget, 'competition', can_add_related = True, can_change_related = True, can_delete_related = True)
		if id:
			result = manager.individually(manager_id, 'C', id)
			self.fields['category'].initial = result.competition_category_id.value
			self.fields['fee'].initial = result.fee.value
			self.fields['prize'].initial = result.prize.value
			self.fields['start_date'].initial = result.start_date.value
			self.fields['end_date'].initial = result.end_date.value
			self.fields['register_low'].initial = result.register_low.value


class LessonForm(forms.Form):
	category = forms.ChoiceField()
	title = forms.CharField(label = 'Сургалт нэр', widget = forms.TextInput(attrs = {'class':'form-control'}))
	url = forms.CharField(label = 'Бичлэгний url хаяг', widget = forms.TextInput(attrs = {'class':'form-control'}))
	author_name = forms.CharField(label = 'Сургалт хийсэн багшийн нэр', widget = forms.TextInput(attrs = {'class':'form-control'}))
	author_email = forms.EmailField(label = 'Сургалт хийсэн багшийн и-мэйл', widget = forms.EmailInput(attrs = {'class':'form-control'}))

	def __init__(self, manager_id = None, type = None, id = None, is_delete = False, *args, **kwargs):
		super(LessonForm, self).__init__(*args, **kwargs)
		self.fields['category'] = forms.ChoiceField(label = u'Ангилал', choices = tuple(manager.show_category(manager_id, type)), widget = forms.Select(attrs = {'class':'form-control', 'style':'width:90%'}))
		widget = self.fields['category'].widget
		if not is_delete:
			self.fields['category'].widget = PopUpWidget(widget, 'lesson', can_add_related = True, can_change_related = True, can_delete_related = True)
		if id:
			result = manager.individually(manager_id, 'L', id)
			self.fields['category'].initial = result.lesson_category_id.value
			self.fields['title'].initial = result.title.value
			self.fields['url'].initial = result.url.value
			self.fields['author_name'].initial = result.author_name.value
			self.fields['author_email'].initial = result.author_email.value

		if is_delete:
			self.fields['category'].widget.attrs = {'class':'form-control'}
			self.fields['category'].disabled = True
			self.fields['title'].disabled = True
			self.fields['url'].disabled = True
			self.fields['author_name'].disabled = True
			self.fields['author_email'].disabled = True


class PasswordUpdateForm(forms.Form):

	old_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Хуучин нууц үг'}))
	new_password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Шинэ нууц үг'}))
	new_password2	 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Шинэ нууц үг давтах'}))


	def clean(self):
		cleaned_data = super(PasswordUpdateForm, self).clean()
		if self.is_valid():
			if cleaned_data['new_password1'] != cleaned_data['new_password2']:
				raise forms.ValidationError(u'Нууц үг таарахгүй байна', code="invalid")
		return cleaned_data

	def save(self, request):
		result = manager.set_password(request.user.id, self.cleaned_data['new_password1'], self.cleaned_data['old_password'], is_create = False)
		return result

class PasswordResetForm(forms.Form):
	email = forms.EmailField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder': 'И-мэйл'}))



class BankForm(forms.Form):
	name = forms.CharField(label = u"Нэр", widget = forms.TextInput(attrs = {'class':'form-control'}))
	short_name = forms.CharField(label = u"Товчилсон нэр", widget = forms.TextInput(attrs = {'class':'form-control'}))
	icon = forms.CharField(label = u"Icon", widget = forms.TextInput(attrs = {'class':'form-control'}))

	def __init__(self, manager_id = None, id = None, is_delete = False, *args, **kwargs):
		super(BankForm, self).__init__(*args, **kwargs)
		if id:
			result = manager.bank(manager_id, 'I', id = id)
			bank = result.bankList.MXManagerSelectAll_Response.MXManagerSelectBankIndividually_Record
			self.fields['name'].initial = bank.name.value
			self.fields['short_name'].initial = bank.short_name.value
			self.fields['icon'].initial = bank.icon.value
			if is_delete:
				self.fields['name'].disabled = True
				self.fields['short_name'].disabled = True
				self.fields['icon'].disabled = True


class CurrencyForm(forms.Form):
	name = forms.CharField(label = u"Нэр", widget = forms.TextInput(attrs = {'class':'form-control'}))
	short_name = forms.CharField(label = u"Товчилсон нэр", widget = forms.TextInput(attrs = {'class':'form-control'}))
	symbol = forms.CharField(label = u"Тэмдэгт", widget = forms.TextInput(attrs = {'class':'form-control'}))
	icon = forms.CharField(label = u"Icon", widget = forms.TextInput(attrs = {'class':'form-control'}))

	def __init__(self, manager_id = None, id = None, is_delete = False, *args, **kwargs):
		super(CurrencyForm, self).__init__(*args, **kwargs)
		if id:
			result = manager.currency(manager_id, 'I', id = id)
			bank = result.currencyList.MXManagerCurrencySelectAll_Response.MXManagerSelectCurrencyIndividually_Record
			self.fields['name'].initial = bank.name.value
			self.fields['short_name'].initial = bank.short_name.value
			self.fields['symbol'].initial = bank.symbol.value
			self.fields['icon'].initial = bank.icon.value
			if is_delete:
				self.fields['name'].disabled = True
				self.fields['short_name'].disabled = True
				self.fields['symbol'].disabled = True
				self.fields['icon'].disabled = True

class CurrencyValueForm(forms.Form):
	bank = forms.ChoiceField()
	currency = forms.ChoiceField()
	buy = forms.CharField(label = u'Авах', widget = forms.TextInput(attrs = {'class':'form-control'}))
	sell = forms.CharField(label = u'Зарах',widget = forms.TextInput(attrs = {'class':'form-control'}))
	
	def __init__(self, manager_id = 0, *args, **kwargs):
		super(CurrencyValueForm, self).__init__(*args, **kwargs)
		bank_list = []
		currency_list = []
		banks = manager.bank(manager_id, 'S')
		currencys = manager.currency(manager_id, 'S')
		for bank in banks:
			b = ('%s'%bank['id'], '%s'%bank['name'])
			bank_list.append(b)
		for currency in currencys:
			c = ('%s'%currency['id'], '%s'% currency['name'])
			currency_list.append(c)
		self.fields['bank'] = forms.ChoiceField(label = u'Банк', choices = tuple(bank_list), widget = forms.Select(attrs = {'class':'form-control'}))
		self.fields['currency'] = forms.ChoiceField(label = u'Валют', choices = tuple(currency_list), widget = forms.Select(attrs = {'class':'form-control'}))


class StockForm(forms.Form):
	name = forms.CharField(label = u"Нэр", widget = forms.TextInput(attrs = {'class':'form-control'}))
	symbol = forms.CharField(label = u"Тэмдэгт", widget = forms.TextInput(attrs = {'class':'form-control'}))
	
	def __init__(self, manager_id = None, id = None, is_delete = False, *args, **kwargs):
		super(StockForm, self).__init__(*args, **kwargs)
		if id:
			result = manager.stock(manager_id, 'I', id = id)
			stock = result.stockList.MXManagerSelectAllStock_Response.MXManagerSelectStockIndividually_Record
			self.fields['name'].initial = stock.name.value
			self.fields['symbol'].initial = stock.symbol.value
			if is_delete:
				self.fields['name'].disabled = True
				self.fields['symbol'].disabled = True

class StockValueForm(forms.Form):
	stock = forms.ChoiceField()
	open = forms.CharField(label = u'Нээлтйин ханш', widget = forms.TextInput(attrs = {'class':'form-control'}))
	buy = forms.CharField(label = u'Авах', widget = forms.TextInput(attrs = {'class':'form-control'}))
	sell = forms.CharField(label = u'Зарах',widget = forms.TextInput(attrs = {'class':'form-control'}))
	high = forms.CharField(label = u'Дээд',widget = forms.TextInput(attrs = {'class':'form-control'}))
	low = forms.CharField(label = u'Доод',widget = forms.TextInput(attrs = {'class':'form-control'}))
	last = forms.CharField(label = u'Сүүлийн',widget = forms.TextInput(attrs = {'class':'form-control'}))
	close = forms.CharField(label = u'Хаалтын ханш',widget = forms.TextInput(attrs = {'class':'form-control'}))
	
	def __init__(self, manager_id = 0, *args, **kwargs):
		super(StockValueForm, self).__init__(*args, **kwargs)
		stock_list = []
		stocks = manager.stock(manager_id, 'S')
		for stock in stocks:
			s = ('%s'%stock['id'], '%s'%stock['name'])
			stock_list.append(s)
		self.fields['stock'] = forms.ChoiceField(label = u'Хувьцаа', choices = tuple(stock_list), widget = forms.Select(attrs = {'class':'form-control'}))

