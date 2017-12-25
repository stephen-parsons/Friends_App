from django.shortcuts import render, redirect
from .models import Users
from django.contrib import messages
import re
import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
	if request.session.get('user_id') != None:	
		return redirect('/friends')
	else:
		return render(request, "login_and_registration_app/index.html")

def process(request):
	if request.method == 'POST':
		new_user = Users.objects.AddUser(
			request.POST['name'],
			request.POST['alias'], 
			request.POST['email'],
			request.POST['dob'],
			request.POST['password'],
			request.POST['confirm']
			)
		print new_user
		if type(new_user) is list:
			for error in new_user:
				messages.add_message(request, messages.ERROR, error)
			return redirect('/')
		else:
			request.session['user_id'] = new_user.id
			return redirect("/friends")
	else:
		return redirect("/")		

def login(request):	
	if request.method == 'POST':
		login = Users.objects.login(
			request.POST['email'],
			request.POST['password']
			)
		if type(login) is unicode:
			messages.add_message(request, messages.ERROR, login)
			return redirect('/')
		else:
			request.session['user_id'] = login.id
			return redirect("/friends")
		return redirect("/")
	else:
		return redirect("/")	

def logout(request):
	request.session.clear()	
	return redirect('/')
	
