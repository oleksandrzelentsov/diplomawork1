from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from terms.models import Term
from terms.mypackage.html_helper import *


def index(request):
	return HttpResponseRedirect('/terms')


def terms(request):
	if request.method == 'GET':
		nav = NavigationItem.get_navigation(request, 0)
		c_dict = {'terms': Term.get_terms(request.user), 'navigation_items': nav}
		context = RequestContext(request, c_dict)
		return render_to_response("bt_terms.html", context)
	else:
		raise Http404("Wrong method %s." % request.method)


def login(request):
	if not isinstance(request.user, AnonymousUser):
		return HttpResponseRedirect('/')
	template_name = 'bt_login_form.html'
	if request.method == 'GET':
		nav = NavigationItem.get_navigation(request, 1)
		context = RequestContext(request, {'navigation_items': nav})
		return render_to_response(template_name, context)
	elif request.method == 'POST':
		# check data
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is None:
			# return the same page with errors if no
			nav = NavigationItem.get_navigation(request, 1)
			alert1 = Alert('<b>Error!</b> Wrong authentication data.', 3)
			context = RequestContext(request, {'navigation_items': nav, 'username': request.POST['username'], 'errors': [alert1]})
			return render_to_response(template_name, context)
		elif not user.is_active:
			nav = NavigationItem.get_navigation(request, 1)
			msg = Message('<b>Sorry!</b> This user is disabled. Contact <a href="mailto:oleksandrzelentsov@gmail.com">admin</a> to resolve this issue.')
			context = RequestContext(request, {'navigation_items': nav, 'username': request.POST['username'], 'errors': [msg]})
			return render_to_response(template_name, context)
		else:
			# authorize if yes and redirect to main page
			auth_login(request, user)
			return HttpResponseRedirect('/')
		pass


def logout(request):
	if not isinstance(request.user, AnonymousUser):
		auth_logout(request)
	return HttpResponseRedirect('/')


def register(request):
	return Http404('Register is not yet implemented.')
