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
	#Page for new Topic
	url(r'^new_topic/$', views.new_topic, name='new_topic'),
	#Page for new Entry
	url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, 
		name='new_entry'),
	#Page for edit Entry
	url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, 
		name='edit_entry'),
]