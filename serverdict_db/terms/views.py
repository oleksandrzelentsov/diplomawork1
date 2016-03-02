from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render_to_response

from terms.models import Term
from terms.mypackage.html_helper import *


def index(request):
	return HttpResponseRedirect('/terms')


def terms(request):
	if request.method == 'GET':
		nav = []
		if isinstance(request.user, AnonymousUser):
			nav += [NavigationItem('Log in', '/login/'), NavigationItem('Sign up', '/signup/')]
		else:
			nav += [NavigationItem('Log out', '/logout/'), NavigationItem('Add term', '/terms/add')]
		c = RequestContext(request, {'terms': Term.get_terms(request.user), 'navigation_items': nav})
		return render_to_response("bt_terms.html", c)
	else:
		raise Http404("Wrong method %s." % request.method)


def login(request):
	# redirect to main if authorized
	if request.method == 'GET':
		# show form here
		pass
	elif request.method == 'POST':
		# validate parameters and check data
		# return the same page with errors if no
		# authorize if yes and redirect to main page
		pass


def logout(request):
	if not isinstance(request.user, AnonymousUser):
		auth_logout(request)
	return HttpResponseRedirect('/')
