from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import RequestContext
from terms.mypackage.html_helper import *
from terms.mypackage.render_methods import *
from terms.mypackage.functions import get_error_page
from django.contrib.auth import logout as auth_logout
import random


def it_works(request):
	main_content = Article('It works!', 'We launched the app.').get_html()
	main_content += ''.join(Article('Article#%i' % (i + 1), random.choice(lipsum)).get_html() for i in range(10))
	method = BasicPageMethod(request, main_content, Sidebar.get_random_sidebars(6), 0)
	return method.render()


def login(request):
	if request.method not in {'GET', 'POST'}:
		return get_error_page('this page (%s) is not available using %s method' % (request.path, request.method))
	if request.method == "GET": # just display the form
		if request.user.is_authenticated():
			return HttpResponseRedirect('/logout')
		else:
			method = FormPageMethod(request, 'form_login.html', 2)
			return method.render()
	elif request.method == "POST": # try to log in
		return get_error_page(msg='authentication with %s:%s' % (request.POST['username'], request.POST['password']))



def error(request):
	if request.method == 'GET' and 'message' in request.GET.keys():
		main_content = Article('Error!', request.GET['message']).get_html()
	else:
		main_content = Article('Error!', '...or maybe not...').get_html()
	method = BasicPageMethod(request, main_content, Sidebar.get_random_sidebars(1))
	return method.render()


def admin(request):
	return HttpResponseRedirect('/admin')


def logout(request):
	if request.user.is_authenticated():
		auth_logout(request)
	return HttpResponseRedirect('/')
