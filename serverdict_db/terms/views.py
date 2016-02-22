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
from django.views.decorators.csrf import csrf_exempt


def it_works(request):
	main_content = my_declarations.Article('It works!', 'We launched the app.').get_html()
	main_content += ''.join(my_declarations.Article('Article#%i' % (i + 1), random.choice(my_declarations.lipsum)).get_html() for i in range(10))
	return my_declarations.get_page(request, main_content, my_declarations.Sidebar.get_random_sidebars(6), 0)

@csrf_exempt # kostyl, needs to be figured out why CSRF does'nt work here
def login(request):
	if request.method not in {'GET', 'POST'}:
		return my_declarations.get_error_page(msg='this page (%s) is not available using %s method' % (request.path, request.method))
	if request.method == "GET": # just display the form
		form = get_template('form_login.html').render({"Navigation": my_declarations.NavigationItem.make_navigation(request, 2)})
		return HttpResponse(form)
	elif request.method == "POST": # try to log in
		return my_declarations.get_error_page(msg='authentication with %s:%s' % (request.POST['username'], request.POST['password']))



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
