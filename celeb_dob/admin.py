from django.contrib import admin
from celeb_dob.models import Celeb

class CelebAdmin(admin.ModelAdmin):
	list_display = ('name', 'dob', 'number_of_hits', 'output_name')

admin.site.register(Celeb, CelebAdmin)
