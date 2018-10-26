from django import forms
from .models import Topic, Entry, Message, CommentProduct, StatsProduct

class TopicForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ['text']
		labels = {'text': ''}


class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		fields = ['name', 'price', 'text', 'file',]
		labels = {'text': ''}
		
		widgets = {
			'name': forms.TextInput(),
			'price': forms.NumberInput(),
			'text': forms.Textarea( attrs={'cols': 80} ), 
		}

class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ['title', 'text']
		labels = {'text': ''}

class CommentProductForm(forms.ModelForm):
	class Meta:
		model = CommentProduct
		fields = ['text',]
		labels = {'text': ''}

class StatsProductForm(forms.ModelForm):
	class Meta:
		model = StatsProduct
		fields = [
			'brand', 
			'type_model', 
			'type_engine', 
			'type_drive', 
			'year_create'
		]
		labels = {'text': ''}	
		