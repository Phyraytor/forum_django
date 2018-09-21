from django.shortcuts import render
from .models import Topic, Entry
# Create your views here.

def index(request):
	"""Home page application Learning Log"""
	return render(request, 'learning_logs/index.html')

def topics(request):
	"""show list topic"""
	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
	"""show this topic and his text"""
	topic = Topic.objects.get(id=topic_id)
	entries = topic.entry_set.all() #order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)