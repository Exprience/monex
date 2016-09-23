# !/usr/bin/python/env
# -*- coding:utf-8 -*-


import jsonpickle




def put(request, name, user):
	request.session[name] = jsonpickle.encode(user)




def get(request, name):
    if name in request.session:
        return jsonpickle.decode(request.session[name])
    else:
        return None




def pop(request, name):
    if name in request.session:
        request.session.pop(name, None)