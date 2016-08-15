import json
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import *

__all__ = ['RoomView', 'ChatView', 'message']

class RoomView(FormView):
	template_name = 'chat/room.html'
	form_class = RoomForm
	success_url = reverse_lazy('room')

	def dispatch(self, request, *args, **kwargs):
		return super(RoomView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(RoomView, self).get_context_data(*args, **kwargs)
		return context

class ChatView(FormView):
	template_name = 'chat/chat.html'
	form_class = MessageForm

	def get_success_url(self, **kwargs):
		return reverse_lazy('chat', args = (self.room_id))

	def dispatch(self, request, *args ,**kwargs):
		self.room_id = self.kwargs.pop('id', None)
		self.user = request.user
		return super(ChatView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(ChatView, self).get_context_data(*args, **kwargs)
		return context

	def form_valid(self, form):
		message = form.save(commit = False)
		message.room = Room.objects.get(id = self.room_id)
		message.user = self.user
		message.save()

		res = {'id':message.id,'msg':message.content,'user':message.user.username,'time':message.date.strftime('%I:%M:%S %p').lstrip('0')}
		data = json.dumps(res)
		return HttpResponse(data,content_type="application/json")

def message(request, id = 0):
	messages = Message.objects.filter(room__id = id)
	c = []
	for m in messages:
		c.append({'user': m.user.username, 'msg': m.content, 'time': m.date.strftime('%I:%M:%S %p').lstrip('0')}) 
	data = json.dumps(c)
	return HttpResponse(data, content_type="application/json")