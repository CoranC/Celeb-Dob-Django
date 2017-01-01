from django import forms
from celeb_dob.models import Celeb

class CelebNameForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Enter Celebrity Name")
	dob = forms.CharField(widget=forms.HiddenInput(), max_length=10)
	number_of_hits = forms.IntegerField(widget=forms.HiddenInput())
	output_name = forms.CharField(widget=forms.HiddenInput(), max_length=128)

	class Meta:
		model = Celeb
		fields = ('name',)
