from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm



def logout_view(request):
	"""Завершает сеанс работы с приложением."""
	logout(request)
	return HttpResponseRedirect( reverse('learning_logs:index') )
def register(request):
	""" Create new users"""
	if request.method != 'POST':
		#Display blank reqistration form.
		form = UserCreationForm()
	else:
		#Обработка заполненной формы.
		form = UserCreationForm(data=request.POST)

		if form.is_valid():
			new_user = form.save()
			#enter and 
