"""определяет схемы URL для learning_logs"""
from django.conf.urls import url

from . import views

urlpatterns = [
	# home page
	url(r'^$', views.index, name='index'),
	# show all topic
	url(r'^topics/$', views.topics, name='topics'),
	# page topics
	url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
	# page for new Topic
	url(r'^new_topic/$', views.new_topic, name='new_topic'),
	# page for new Entry
	url(r'^new_entry/$', views.new_entry, name='new_entry'),
	# page for edit Entry
	url(r'^edit_entry/(?P<entry_id>\d+)/$', 
		views.edit_entry, name='edit_entry'),
	# page product
	url(r'^product/(?P<product_id>\d+)/$', views.product, name='product'),

	# add comment product
	url(r'^product/comment/(?P<product_id>\d+)/$', views.comment_product, name='comment_product'),
	# page full text for topic
	url(r'^account/$', views.account, name='account'),
	# page full text for topic
	url(r'^account/(?P<account_id>\d+)/$', views.accounts, name='accounts'),
	# page messages
	url(r'^account/messages/$', views.messages, name='messages'),
	# page messages
	url(r'^account/send_message/(?P<address_id>\d+)/$', views.send_message, name='send_message'),
	
	
]