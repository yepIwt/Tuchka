from django.db import models

class Support(models.Model):
	name = models.CharField('nickname', max_length = 200, default='user<3')
	date = models.DateTimeField('date')
	
	def __str__(self):
		return self.name
