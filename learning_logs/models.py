from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
	"""This topic look user"""
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	#owner = models.ForeignKey(User)
	def __str__(self):
		return self.text

class Entry(models.Model):
	"""Information, reading user this topic"""
	topic = models.ForeignKey(Topic)
	text = models.TextField()
	data_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User)
	class Meta:
		verbose_name_plural = 'entries'

	def __str__(self):
		if len(self.text) <= 50: 
			return self.text
		else: 
			return self.text[:50] + "..."

		