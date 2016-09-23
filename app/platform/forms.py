# -*- coding: utf-8 -*-
from django import forms


class PriceAlertForm(forms.Form):
	ALERT_CHOICES = (
		('Авах үнэ', 'Buy Price'),
		('Зарах үнэ', 'Sell Price'),)
	alert_type = forms.ChoiceField(choices = ALERT_CHOICES, label='Alert Type',  widget = forms.Select(attrs = {'class':"form-control", 'float':"right"}))
	CONDITION_CHOICES = (
		('>=', '>='),
		('<=', '<='),)
	condition = forms.ChoiceField(choices = CONDITION_CHOICES, label='Condition', widget = forms.Select(attrs = {'class':"form-control"}))
	
	ACTIVE_CHOICES = (
    	('ON', 'ON'),
    	('OFF', 'OFF'),)
	active = forms.ChoiceField(choices = ACTIVE_CHOICES,label='Active', widget = forms.Select(attrs = {'class':"form-control"}))
	price = forms.CharField(label='Price', widget = forms.TextInput(attrs = {'class':"form-control",'placeholder':'Value'}))
	exp_date = forms.DateField(label='Expire Date',widget = forms.DateInput(attrs = {'class':"form-control",'style': 'height:30px', 'font-color':'black'}))
	comment = forms.CharField(label='Comment',max_length=300, widget = forms.TextInput(attrs = {'class':"form-control", 'style': 'height: 70px','placeholder':'Comment'}))


class BuyFrom(forms.Form):
	currency = forms.ChoiceField()
	bank = forms.ChoiceField()
	quantity = forms.IntegerField()


class OrderForm(forms.Form):
	Currency_Choices = (
		('usa','USD/MNT'),
		('eur','EUR/MNT'),
		('xxx','XXX/MNT'),
		('lll','LLL/MNT'),
		('ooo','OOO/MNT'),
		)
	currency = forms.ChoiceField(choices = Currency_Choices)
	Bank_Choices = (
		('Haan','Хаан Банк'),
		('Golomt','Голомт Банк'),
		('Turiin','Төрийн Банк'),
		('x','хххххххххх'),
		('c','ччччччччччччч'),
		)
	bank = forms.ChoiceField(choices = Bank_Choices)
	quantity = forms.IntegerField()
	Order_Choices = (
		('limited','Хязрааласан үнээр'),
		('Now','Зах зээлийн үнээр'),
		)
	order_type = forms.ChoiceField(choices = Order_Choices)
	B_Choices = (
		('SELL','Зарах'),
		('BUY','Авах'),
		)
	buy_sell = forms.ChoiceField(choices = B_Choices)
	exp_date = forms.ChoiceField()
class AccountForm (forms.Form):
	sur_name = forms.CharField(label='Овог', widget = forms.TextInput(attrs = {'class':"form-control",'placeholder':'Value'}))
	name = forms.CharField(label='Нэр', widget = forms.TextInput(attrs = {'class':"form-control",'placeholder':'Value'}))
	rd = forms.CharField(label='Регистерийн дугаар', widget = forms.TextInput(attrs = {'class':"form-control",'placeholder':'Value'}))
	birth_date = forms.DateField(label='Төрсөн Огноо',widget = forms.DateInput(attrs = {'class':"form-control",'style': 'height:30px', 'font-color':'black'}))
	G_Choices = (
		('male','Эрэгтэй'),
		('female','Эмэгтэй'),
		)
	gender = forms.ChoiceField(choices = G_Choices)
	address = forms.CharField(label='Хаяг',max_length=300, widget = forms.TextInput(attrs = {'class':"form-control", 'style': 'height: 70px','placeholder':'Хаяг'}))
	email = forms.EmailField(label='И-Майл',max_length=300, widget = forms.EmailInput(attrs = {'class':"form-control", 'style': 'height: 70px','placeholder':'Майл'}))
	phone2 = forms.CharField(label='Утас', widget = forms.TextInput(attrs = {'class':"form-control",'placeholder':'Value'}))
	phone2 = forms.CharField(label='Утас', widget = forms.TextInput(attrs = {'class':"form-control",'placeholder':'Value'}))