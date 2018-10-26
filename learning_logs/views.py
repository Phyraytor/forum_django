from django.shortcuts import render, render_to_response

from django.template.defaulttags import register 
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.translation import ugettext_lazy

from .models import Topic, Entry, User, Message, CommentProduct, StatsProduct, StatsProductList
from .forms import TopicForm, EntryForm, MessageForm, CommentProductForm, StatsProductForm

#consts
COUNT_PRODUCTS_PAGE = 5
COUNT_MESSAGE_PAGE = 5


@register.filter 
def get_item(dictionary, key):
	""" Это нужно для перевода""" 
    return dictionary.get(key)

# Create your views here.

def index(request):
	"""Home page application Learning Log"""
	return render(request, 'learning_logs/index.html')

 #так видит только владелец статьи
@login_required
def account(request):
	"""show list topic"""
	topic = Topic.objects.first()
	entries = Entry.objects.filter(owner=request.user) 
	entries = this_page(request, entries, COUNT_PRODUCTS_PAGE)
	entries.url = '/account'
	context = {
		'topics': topic, 
		'entries': entries,
		'elements': entries,
	}
	return render(request, 'learning_logs/account.html', context)

def accounts(request, account_id):
	"""show list topic"""
	# Если это личный кабинет текущего пользователя - перейти в его кабинет
	if int(account_id) == int(request.user.id)	:
		return HttpResponseRedirect( reverse('learning_logs:account') )
	topic = Topic.objects.first()	
	the_user = User.objects.get(id=account_id)
	entries = Entry.objects.filter(owner=the_user) 
	entries = this_page(request, entries, COUNT_PRODUCTS_PAGE)
	entries.url = '/account/' + account_id + '/'
	context = {
		'topics': topic, 
		'entries': entries, 
		'the_user': the_user, 
		'elements': entries,
	}
	return render(request, 'learning_logs/accounts.html', context)

def messages(request):
	"""show list messages"""
	my_messages = Message.objects.filter(address_id=request.user.id)
	my_messages = this_page(request, my_messages, COUNT_MESSAGE_PAGE)
	my_messages.url = "/account/messages"
	context = {'messages': my_messages, 'elements': my_messages}
	return render(request, 'learning_logs/messages.html', context) 

def topics(request):
	"""show list topic"""
	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
	"""show this topic and his text"""
	topic = Topic.objects.get(id=topic_id)
	products = topic.entry_set.all() #order_by('-date_added')
	products = filter_products(request, products)
	products = this_page(request, products, COUNT_PRODUCTS_PAGE)
	filters = create_filters_list()
	GET = create_get_url(request)
	products.url = "/topics/" + topic_id + "/"
	translate_filter = {
		'Brand': 'Марка', 
		'Type_model': 'Модель', 
		'Type_engine': 'Двигатель', 
		'Type_drive': 'Привод', 
		'Year_create': 'Год' 
	}
	context = {
		'topic': topic, 
		'products': products, 
		'filters': filters,
		'GET': GET,
		'translate_filter': translate_filter,
		'elements': products,  
	}
	return render(request, 'learning_logs/topic.html', context)

def product(request, product_id):
	"""show this product and his text"""
	obj_product = Entry.objects.get(id=product_id)
	comments = CommentProduct.objects.filter(product=obj_product)
	comments = this_page(request, comments, COUNT_MESSAGE_PAGE)
	comments.url = "/product/" + product_id + "/"
	context = {
		'product': obj_product, 
		'comments': comments, 
		'elements': comments
	}
	return render(request, 'learning_logs/product.html', context)


''' *********************************functions form *************************************'''
@login_required
def send_message(request, address_id):
	""" Отправляет сообщение пользователю """
	if request.method != 'POST':
		# Data not send, create empty form
		form = MessageForm()
	else:
		#Data send; tread data
		form = MessageForm(request.POST)
		if form.is_valid():
			new_message = form.save(commit=False)
			new_message.address_id = address_id
			new_message.sender = request.user
			new_message.save()
			return HttpResponseRedirect( reverse('learning_logs:account'))
	context = {'form': form, 'address': address_id}
	return render(request, 'learning_logs/send_message.html', context)

@login_required
def comment_product(request, product_id):
	""" Оставить комментарий под товаром """
	if request.method != 'POST':
		# Data not send, create empty form
		form = CommentProductForm()
	else:
		#Data send; tread data
		form = CommentProductForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.product = Entry.objects.get(id=product_id)
			new_comment.commenter = request.user
			new_comment.save()
			return HttpResponseRedirect( reverse('learning_logs:topics'))
	context = {'form': form, 'product': product_id}
	return render(request, 'learning_logs/comment_product.html', context)


@login_required
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

@login_required	
def new_entry(request):
	"""Определяет новое сообщение"""
	topic = Topic.objects.get(id=1)
	if request.method != 'POST':
		#Data not send, create empty form
		form = EntryForm()
	else:
		#Data send; tread data

		post_product = add_filters_product(request)
		form = EntryForm(post_product, request.FILES)
		if form.is_valid():
			new_enrty = form.save(commit=False)
			new_enrty.topic = topic
			new_enrty.owner = request.user
			new_enrty.stats = StatsProduct.objects.last()
			#new_enrty.text = name_row + value_rown
			new_enrty.save()
			return HttpResponseRedirect( reverse('learning_logs:account') )
	filters = create_filters_list()
	context = {'topic': topic, 'form': form, 'filters': filters}
	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	"""Определяет новое сообщение"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if entry.owner != request.user:
		raise Http404
	if request.method != 'POST':
		#Data not send, create empty form
		form = EntryForm(instance=entry)
	else:
		#Data send; tread data
		post_product = add_filters_product(request, True)
		form = EntryForm(request.POST, request.FILES, instance=entry)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect( reverse('learning_logs:account') )
	filters = create_filters_list()
	context = {'entry': entry, 'topic': topic, 'form': form, 'filters': filters}
	return render(request, 'learning_logs/edit_entry.html', context)	

''' ************************************closes funcions *************************'''

def this_page(request, items, count):
	""" paginator """
	if "page" in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	pag = Paginator(items, count)
	try:
		result = pag.page(page_num)
	except:
		result = pag.page(1)
	return result

def create_filters_list():
	""" Полный список фильтров отсортированный по ключам """

	filters = StatsProductList.objects.all()
	result = {}
	for key_filter in filters:
		if key_filter.key in result:
			result[key_filter.key].append(key_filter.value)
		else:
			result[key_filter.key] = [key_filter.value]
	return result


def filter_products(request, products):
	""" Фильтры товаров """
	list_filter = clear_bad_get(request)
	result = []
	for product in products:
		if check_filter(list_filter, product):
			result.append(product)
	return result

def clear_bad_get(request):
	""" Исключить не нужные get данные """
	list_filter = {}
	for key in request.GET:
		if request.GET[key] != '' and  key.lower() != 'page':
			list_filter[key] = request.GET[key]
	return list_filter

def check_filter(list_filter, product):
	for key_get in list_filter:
		if getattr(product.stats, key_get.lower() ) != list_filter[key_get]:
			return False
	return True

def add_filters_product(request, edit = False):
	post_product = {}
	keys = ('name', 'price', 'text')
	for key in keys:
		post_product[key] = request.POST[key]
		request.POST.pop(key)
	request.POST = {k.lower(): v for k, v in request.POST.items()}
	if edit:
		form = StatsProductForm(request.POST, instance=entry)
	else:
		form = StatsProductForm(request.POST)
	if form.is_valid():
		form.save()
	return post_product

def create_get_url(request):
	GET = ""
	for key, value in request.GET.items():
		if key.lower() != 'page':
			GET += "&" + key + "=" + value
	return GET
#неудавшаяся попытка сделать дабавление товара через SQL запрос
#name_row = "(" + ", ".join(request.POST.keys() ) + ")"
		#value_rown = " (NULL, '" + "', '".join( request.POST.values() )  + "')"
		#StatsProduct.objects.raw("INSERT INTO learning_logs_StatsProduct (" + name_row + ") VALUES (" + value_rown + ")" )
