from django.db import models

class File(models.Model):
	date = models.DateTimeField('date')
	save = models.BooleanField('save', default=False)
	hash = models.TextField('hash', default = '0')
	bits = models.TextField('bits', default = '0')

	def data(self):
		if self.save:
			return [self.hash,self.bits]
		else:
			return False

	def __str__(self):
		return self.data()

#n = ['vk.com/ewfwfe','vk.com/2tr23r','pornhub.com/videos']
#a = set(n)
#list(b)
