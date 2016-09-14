# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import math


def convert_2_10(create, update, delete):
	num1 = 0
	num2 = 0
	num3 = 0
	
	if create != 0:
		num1 = math.pow(2, 2)

	if update != 0:
		num2 = math.pow(2, 1)

	if delete != 0:
		num3 = math.pow(2, 0)

	return int(num1 + num2 + num3)


def convert_10_2(value):
	list = []
	for i in str(format(int(value), '#05b')):
		list.append(str(i))
	list = list[2:5]
	return list


def get_dict(values):
	lists = []
	for value in values:
		context = {}
		for key in value.__keylist__:
			context[key] = getattr(value, key).value
		lists.append(context)
	return lists