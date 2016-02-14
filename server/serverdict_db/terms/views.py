from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Q
from django.shortcuts import render
from terms import my_declarations
import random
import django.contrib.auth as auth
from django.contrib.auth.forms import AuthenticationForm


def it_works(request):
	main_content = my_declarations.Article('It works!', 'We launched the app.').get_html()
	main_content += ''.join(my_declarations.Article('Article#%i' % (i + 1), random.choice(my_declarations.lipsum)).get_html() for i in range(10))
	return my_declarations.get_page(request, main_content, my_declarations.Sidebar.get_random_sidebars(6), 0)


def login(request):
	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if form.is_valid() and user:
			auth.login(request, user)
			return HttpResponseRedirect('/')
		else:
			return my_declarations.get_error_page('invalid form with data %s:%s' % (username, password))
	else:
		form = AuthenticationForm()
		form_html = get_template('form.html').render(request,
		{
		'form': form,
		'data':
		{'method': 'post', 'submit_text': 'login', 'action': '/login/'}})
		return my_declarations.get_page(request, my_declarations.Article('Authentication', form_html).get_html(), my_declarations.Sidebar.get_random_sidebars(2), 2)


def error(request):
	if request.method == 'GET' and 'message' in request.GET.keys():
		main_content = my_declarations.Article('Error!', request.GET['message']).get_html()
	else:
		main_content = my_declarations.Article('Error!', '...or maybe not...').get_html()
	return my_declarations.get_page(request, main_content, my_declarations.Sidebar.get_random_sidebars(1))


def search(request):
	if request.method == 'GET':
		return my_declarations.get_error_page('it is GET but it\'s not supposed to work')
		if parameters:
		    pass # yield
		else:
			pass
	else:
		return my_declarations.get_error_page('it\'s not GET and it\'s not supposed to work')

def admin(request):
	return HttpResponseRedirect('/admin')
