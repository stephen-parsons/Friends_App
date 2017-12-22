from __future__ import unicode_literals

from django.db import models

from ..login_and_registration_app.models import Users, UserValidator

class Message(models.Model):
	message = models.TextField(max_length=255)
	user = models.ForeignKey(Users, related_name="messages")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	def __repr__(self):
		return "<Message object: {} {}>".format(self.message, self.user.alias)

class Comment(models.Model):
	comment = models.TextField(max_length=255)
	user = models.ForeignKey(Users, related_name="comments")
	message = models.ForeignKey(Message, related_name="comments")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	def __repr__(self):
		return "<Comment object: {} {} {}>".format(self.comment, self.user.alias, self.message)

class Document(models.Model):
	description = models.CharField(max_length=255, blank=True)
	document = models.FileField(upload_to='documents/gifs')
	message = models.ForeignKey(Message, related_name="uploads")
	uploaded_at = models.DateTimeField(auto_now_add=True)		

