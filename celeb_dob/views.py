from django.shortcuts import render
from celeb_dob.models import Celeb
from celeb_dob.forms import CelebNameForm
import requests
import re
import random
import datetime as d


def home(request):
	# Construct a dictionary to pass to the template engine as it's context
	# In simple terms, a template context is essentially a Python dictionary that maps template variable names with Python variables.
	context_dict = {}
	# Here we queried the Category model to retrieve the top five categories.
	# Then we used the order_by() method to sort by the number of likes (descending order utilizing the '-'), (Restriced to first 5 category objects in list)
	# With the query complete, we passed a reference to the list (stored as variable category_list) to the dictionary, context_dict.
	# This dictionary is then passed as part of the context for the template engine in the render() call.
	# Return a rendered response to send to the client.
	return render(request, 'celeb_dob/home.html', context_dict)


def get_celebrity(request):
	context_dict = {}
	context_dict = search_for_celeb(request)
	return render(request, 'celeb_dob/get_celebrity.html', context_dict)


def search_for_celeb(request):
	print "* search_for_celeb view started"
	celeb_result = ""
	if request.method == 'POST':
		input_name = request.POST.get('input_name')
		searchable_name = clean_name(input_name)
		output_name = searchable_name.replace("_", " ")
		# search for celeb in database
		celeb_result = search_name_in_database(searchable_name)
		if not celeb_result:
			# search for celeb using wikipedia API
			print "* searching for celeb in API"
			json = request_json_from_api(searchable_name)
			birthdate = get_birthdate_from_json_result(json)
			if birthdate:
				Celeb.objects.get_or_create(name = searchable_name, dob = birthdate,
						number_of_hits = 0)
				celeb_result = Celeb.objects.filter(name = searchable_name)[0]
				celeb_result.output_name = output_name
	if celeb_result:
		age = get_years_since_birthdate(celeb_result.dob)
		first_name = celeb_result.output_name[:celeb_result.output_name.find(" ")]
		context_dict = {'celebrities': celeb_result, 'age': age, 'first_name':
				first_name}
		related_birthdays = find_related_birthdays(searchable_name,
					celeb_result.dob)
		if related_birthdays:
			context_dict['related_birthdays'] = related_birthdays
	else:
		num = random.choice(range(1,11))
		src = 'images/dontknow{num}.jpg'.format(num=num)
		context_dict = {'random_number' : src}
	return context_dict

def home_form(request):
	if request.method == 'POST':
		form = CelebNameForm(request.POST)
		return search_for_celeb(request)
	else:
		form = CelebNameForm()
	return render(request, 'rango/add_category.html', {'form': form})


def clean_name(name):
	"""
	Takes in an input string from a user and returns a string formatted to be searched by the API.
	e.g. 'harry hill' becomes 'Harry_Hill'
	Args: param1 (str): name.
	Returns: (str): name_to_search
	"""
	name = str(name)
	name_trailing_white_space_removed = name.strip()
	name_spaces_corrected = re.sub('\s+', '_', name_trailing_white_space_removed) # Replace multiple spaces with just one space
	name_to_search = name_spaces_corrected.title() # Capitalizes all First Letters of words
	return name_to_search


def request_json_from_api(clean_name_to_search):
	"""
	Takes in a clean name to search and queries the api returning a string of json data. 
	Args: param1 (str): clean_name_to_search
	Returns: (str): str(json)
	"""
	print "clean_name_to_search: {}".format(clean_name_to_search)
	url_string = "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=" + clean_name_to_search + "&rvprop=content&format=json"
	r = requests.get(url_string)
	full_json_result = str(r.json())
	print full_json_result
	return full_json_result


def get_birthdate_from_json_result(json_result):
	"""
	Takes in a string of json data and uses a regex to search for the date of birth
	Args: param1 (str): json
	Returns: (str): date of birth
	"""
	# Looks for case insensitive 'Birth Date' [with optional ' and age'] with '|' [with optinal 'mf=yes'] with 'YYYY|MM|DD'
	birthPattern = 'Birth date( and age)?\|(\w+=\w+\|)?(\d{1,4}\|\d{1,2}\|\d{1,2})'
	match = re.search(birthPattern, json_result, flags=re.IGNORECASE)
	if not match:
		return None
	else:
		result = ""
		for group in match.groups():
			if group:
				result = group
		birthdate_before_format = result
		birthdate = birthdate_before_format.replace('|', "/")
		birthdate = birthdate.replace("/0", "/")
		return birthdate


def get_years_since_birthdate(birthdate):
	"""
	Coverts data of birth to number of years since that date.
	Args: param1 (str): birthdate
	Returns: (int): number_of_years
	"""
	celeb_birthdate = d.datetime.strptime(birthdate, "%Y/%m/%d").date()
	today_date = d.date.today()
	date_delta = today_date - celeb_birthdate
	number_of_years = date_delta.days / 365
	return number_of_years


def search_name_in_database(searchable_name):
	try:
		celeb_result = Celeb.objects.get(name = searchable_name)
		celeb_result.number_of_hits += 1
		celeb_result.save()
		return celeb_result
	except Celeb.DoesNotExist:
		return None


def find_related_birthdays(celeb_name, birthdate):
	birthdate_substring = birthdate[4:]
	try:
		related_birthdays_list = Celeb.objects.filter(
			dob__endswith = birthdate_substring).exclude(name = celeb_name).order_by('-number_of_hits')[:5]
		return related_birthdays_list
	except:
		print None
