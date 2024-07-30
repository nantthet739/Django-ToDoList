from django.db import models
from django.contrib.auth.models import User #built in user model use

# Create your models here.

class Task(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE,null = True, blank = True)
	title = models.CharField(max_length = 200)
	description = models.TextField(null = True, blank = True) # want box so Text
	complete = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True) #auto populate

	def __str__(self):
		return self.title #default value is title

	class Meta:
		ordering = ['complete']
