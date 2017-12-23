from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Message, Comment, Document
from ..login_and_registration_app.models import Users
from .forms import DocumentForm
from django.conf import settings
import os

def index(request):
	if request.session.get('user_id') != None:
		user = Users.objects.get(id=request.session['user_id'])
		message_list = Message.objects.all()
		comments = Comment.objects.all()
		uploads = Document.objects.all()
		length = len(message_list) - 1
		context = {
			"user" : user, 
			'message_list' : message_list, 
			'comments' : comments,
			"length" : length,
			"uploads" : uploads
			}
		return render(request, "wall_app/test.html", context)
	else:
		return redirect("/")
			

def submit_message(request):
	if request.method == "POST":
		# check if message is blank: 
		if str(request.POST['message']) == "":
			error = "Message cannot be blank!"		
			messages.add_message(request, messages.ERROR, error)
		else:	
			if request.FILES:
				file = request.FILES['file']
				if not file.name.endswith('.gif'):
					error = "File can only be .gif!"		
					messages.add_message(request, messages.ERROR, error)
				elif file.size > int(settings.MAX_UPLOAD_SIZE):
					error = "Your file is too dang big!"		
					messages.add_message(request, messages.ERROR, error)	
				else:
					new_message = Message.objects.create(
					message=request.POST['message'],
					user= Users.objects.get(id=request.session['user_id'])
					)
					form = Document.objects.create(description=request.POST, document=request.FILES['file'], message=new_message)
			else:
				error = "Must include .gif!"		
				messages.add_message(request, messages.ERROR, error)	
		return redirect('/wall')
	else:
		return redirect('/wall')	

def delete_msg(request):
	if request.method == "POST":
		message = Message.objects.get(id=request.POST['message_id'])
		comment = Comment.objects.filter(message = message)
		upload = Document.objects.filter(message = message).first()
		#delete file, then comments then message
		if upload != None:
			os.remove(upload.document.path)
			upload.delete()	
		comment.delete()
		message.delete()
		return redirect('/wall')
	else:
		return redirect('/wall')		 		

def submit_comment(request):
	if request.method == "POST":
		# check if comment is blank:
		if str(request.POST['comment']) == "":
			error = "Comment cannot be blank!"		
			messages.add_message(request, messages.ERROR, error)
		else:	
			new_comment = Comment.objects.create(
				comment=request.POST['comment'],
				message=Message.objects.get(id=request.POST['message_id']),
				user=Users.objects.get(id=request.session['user_id'])
				)
		return redirect('/wall')
	else:
		return redirect('/wall')		

def delete_comment(request):
	if request.method == "POST":
		comment = Comment.objects.get(id=request.POST['comment_id'])
		comment.delete()
		return redirect('/wall')
	else:
		return redirect('/wall')			
