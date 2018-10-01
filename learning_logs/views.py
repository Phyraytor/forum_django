
from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

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

def new_topic(request):
	"""Определяет новую тему"""
	if request.method != 'POST':
		# Data not send, create empty form
		form = TopicForm()
	else:
		#Data send; tread data
		form = TopicForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect( reverse('learning_logs:topics') )

	context = {'form': form}	
	return render(request, 'learning_logs/new_topic.html', context)
	
def new_entry(request, topic_id):
	"""Определяет новое сообщение"""
	topic = Topic.objects.get(id=topic_id)
	if request.method != 'POST':
		#Data not send, create empty form
		form = EntryForm()
	else:
		#Data send; tread data
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_enrty = form.save(commit=False)
			new_enrty.topic = topic
			new_enrty.save()
			return HttpResponseRedirect( reverse('learning_logs:topic', 
				args=[topic_id]) )
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
	"""Определяет новое сообщение"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if request.method != 'POST':
		#Data not send, create empty form
		form = EntryForm(instance=entry)
	else:
		#Data send; tread data
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect( reverse('learning_logs:topic', 
				args=[topic.id]) )
	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)