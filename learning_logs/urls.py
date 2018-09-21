"""определяет схемы URL для learning_logs"""
from django.conf.urls import url

from . import views

urlpatterns = [
	#home page
	url(r'^$', views.index, name='index'),

	#show all topic
	url(r'^topics/$', views.topics, name='topics'),
	#page full text for topic
	url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
]