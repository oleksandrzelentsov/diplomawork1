from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template

from terms.models import Term
from terms.mypackage.html_helper import *


def index(request):
    return HttpResponseRedirect('/terms')


def terms(request):
    if request.method == 'GET':
        nav = NavigationItem.get_navigation(request, 0)
        c_dict = {'terms': Term.get_terms(request.user), 'navigation_items': nav}
        context = RequestContext(request, c_dict)
        return get_template("bt_terms.html").render(context)
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
            context = RequestContext(request, {'navigation_items': nav, 'username': request.POST['username'],
                                               'errors': [alert1]})
            return render_to_response(template_name, context)
        elif not user.is_active:
            nav = NavigationItem.get_navigation(request, 1)
            msg = Alert(
                '<b>Sorry!</b> This user is disabled. Contact <a href="mailto:oleksandrzelentsov@gmail.com">'
                'admin</a> to resolve this issue.')
            context = RequestContext(request,
                                     {'navigation_items': nav, 'username': request.POST['username'], 'errors': [msg]})
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
    if request.method == 'GET':
        if request.user.is_authenticated():
            HttpResponseRedirect('/')
        else:
            # show register form
            pass
    elif request.method == 'POST':
        # check parameters
        # collect errors
        # if there are any errors, return the same page with them
        # if everything is okay, check if the user with the same
        # email or username is present
        pass
    else:
        return Http404()
