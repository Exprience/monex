# !/usr/bin/env/python
# -*- coding:utf-8 -*-


from redactor.handlers import SimpleUploader
from managers import BaseDataManager as cm
from app.manager.models import FileInput
from django.core.urlresolvers import reverse_lazy


class NewsUploader(SimpleUploader):

	def save_file(self):
		super(NewsUploader, self).save_file()
		file = FileInput.objects.create(file = self.upload_file).file
		pattern = cm.file_upload("N", "1" , file.name, file.path).pattern
		if not hasattr(self, "pattern"):
			self.pattern = pattern

	def get_url(self):
		return reverse_lazy("file", kwargs = {'file': self.pattern})
