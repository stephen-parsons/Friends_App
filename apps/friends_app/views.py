from django.shortcuts import render, redirect
from ..login_and_registration_app.models import Users
from .models import Image, Requests
from django.contrib import messages
from django.conf import settings
import os

def index(request):
	if request.session.get('user_id') != None:
		empty = False
		if Users.objects.all().count() <= 1:
			empty = True
		user = Users.objects.get(id=request.session['user_id'])
		friends = user.friends.all()
		recieved_requests = user.recieved_requests.all()
		images = Image.objects.all()
		check_recieved_requests = [some_request.sending_request.id for some_request in recieved_requests]
		sent_requests = user.sent_requests.all()
		check_sent_requests = [some_request.recieving_request for some_request in sent_requests]
		not_friends = Users.objects.all().exclude(id=user.id).exclude(id__in=friends).exclude(id__in=check_recieved_requests)
		context = {
			"user" : user, 
			"not_friends" : not_friends, 
			'empty' : empty, 
			'recieved_requests' : recieved_requests, 
			"sent_requests" : check_sent_requests,
			"images" : images
			}
		return render(request, "friends_app/index.html", context)
	else:
		return redirect("/")		

def send_request(request, user_id):
	if request.method == "POST":
		sending_user = Users.objects.get(id=request.session['user_id'])
		recieving_user = Users.objects.get(id=user_id)
		new_request = Requests.objects.create(sending_request=sending_user, recieving_request=recieving_user)
		return redirect('/friends')
	else:
		return redirect("/friends")	

def cancel_request(request, user_id):	
	if request.method == "POST":
		user = Users.objects.get(id=request.session['user_id'])
		friend = Users.objects.get(id=user_id)
		request = friend.recieved_requests.filter(sending_request=user)
		request.delete()
		return redirect('/friends')
	else:
		return redirect("/friends")	

def cancel_recieved_request(request, user_id):	
	if request.method == "POST":
		user = Users.objects.get(id=request.session['user_id'])
		friend = Users.objects.get(id=user_id)
		request = user.recieved_requests.filter(sending_request=friend)
		request.delete()
		return redirect('/friends')	
	else:
		return redirect("/friends")	

def add_friend(request, user_id):
	if request.method == "POST":
		user = Users.objects.get(id=request.session['user_id'])
		friend = Users.objects.get(id=user_id)
		user.friends.add(friend)
		request = user.recieved_requests.filter(sending_request=friend)
		request.delete()
		return redirect('/friends')
	else:
		return redirect("/friends")

def un_friend(request, user_id):
	if request.method == "POST":
		user = Users.objects.get(id=request.session['user_id'])		
		friend = Users.objects.get(id=user_id)
		user.friends.remove(friend)
		return redirect('/friends')
	else:
		return redirect("/friends")	

def user_profile(request, user_id):
	if request.session.get('user_id') != None:
		current_user = False
		user = Users.objects.get(id=request.session['user_id'])
		profile = Users.objects.get(id=user_id)
		images = Image.objects.filter(user=profile)
		if int(user_id) == user.id:
			current_user = True
		return render(request, "friends_app/user_profile.html", {"user" : user, "images" : images, 'current_user' : current_user, "profile" : profile})
	else:
		return redirect("/friends")

def upload_picture(request):
	if request.method == "POST":
		user = Users.objects.get(id=request.POST['user_id'])
		if request.FILES:
			file = request.FILES['file']
			if file.content_type.split('/')[0] != 'image':
				error = "File must be image!"		
				messages.add_message(request, messages.ERROR, error)
			elif file.size > int(settings.MAX_UPLOAD_SIZE):
				error = "Your file is too dang big!"		
				messages.add_message(request, messages.ERROR, error)	
			else:
				new_image = Image.objects.create(image = request.FILES['file'], user=user)
		return redirect("/user/{}".format(user.id))	
	else:
		if request.session.get('user_id') == None:
			return redirect("/friends")
		else:
			return redirect("/user/{}".format(user.id))	

def delete_picture(request):
	if request.method == "POST":
		user = Users.objects.get(id=request.POST['user_id'])
		upload = Image.objects.get(id=request.POST['image_id'])
		#delete file
		os.remove(upload.image.path)
		upload.delete()
		return redirect("/user/{}".format(user.id)) 
	else:
		if request.session.get('user_id') == None:
			return redirect("/friends")
		else:
			return redirect("/user/{}".format(user.id))			

