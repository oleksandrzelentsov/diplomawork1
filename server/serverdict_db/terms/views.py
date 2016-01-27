from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Q
from django.shortcuts import render_to_response
from terms import my_declarations
# Create your views here.


def display(request, text):
	return HttpResponse(get_template('base_test.html').render({'Content': text}))

def it_works(request):
	main_content = my_declarations.Article('It works!', 'We launched the app.').get_html()
	return my_declarations.get_page(request, main_content, my_declarations.Sidebar.get_random_sidebars(3), 0)


def template(request, text):
	return HttpResponse(get_template(text + '.html').render({}))
