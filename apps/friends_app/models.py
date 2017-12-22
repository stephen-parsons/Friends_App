from __future__ import unicode_literals

from ..login_and_registration_app.models import Users

from django.db import models

class Requests(models.Model):
	sending_request = models.ForeignKey(Users, related_name="sent_requests")
	recieving_request = models.ForeignKey(Users, related_name="recieved_requests")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	def __repr__(self):
		return "<Requests object: {} {}>".format(self.sending_request.id, self.recieving_request.id)

class Image(models.Model):
	image = models.ImageField(upload_to="documents/user_images")
	user = models.ForeignKey(Users, related_name="uploads")
	uploaded_at = models.DateTimeField(auto_now_add=True)
