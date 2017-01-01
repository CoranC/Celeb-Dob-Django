from django.db import models

class Celeb(models.Model):
	name = models.CharField(max_length=128, unique=True)
	dob = models.CharField(max_length=10)
	number_of_hits = models.IntegerField(default=0)
	output_name = models.CharField(max_length=128,default="")

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.output_name = self.name.replace('_', ' ')
		super(Celeb, self).save(*args, **kwargs)

