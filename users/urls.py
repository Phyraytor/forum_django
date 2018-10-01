from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns = [
	#Page enter
	url(r'^login/$', login, {'template_name': 'users/login.html'},
		name='login'),
	#Page exit
	url(r'^logout/$', views.logout_view, name='logout'),
	#Page register
	url(r'^register/$', views.register, name='register'),
]