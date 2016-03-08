from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
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
        return HttpResponse(get_template("bt_terms.html").render(context=c_dict, request=request))
    else:
        return error(request, '%s method is not allowed for this page' % request.method)


def login(request):
    if not isinstance(request.user, AnonymousUser):
        return HttpResponseRedirect('/')
    template_name = 'bt_login_form.html'
    if request.method == 'GET':
        nav = NavigationItem.get_navigation(request, 1)
        return HttpResponse(get_template(template_name).render(context={'navigation_items': nav}, request=request))
    elif request.method == 'POST':
        # check data
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            # return the same page with errors if no
            nav = NavigationItem.get_navigation(request, 1)
            alert1 = Alert('<b>Error!</b> Wrong authentication data.', 3)
            context = {'navigation_items': nav, 'username': request.POST['username'],
                       'errors': [alert1]}
            return HttpResponse(get_template(template_name).render(context=context, request=request))
        elif not user.is_active:
            nav = NavigationItem.get_navigation(request, 1)
            msg = Alert(
                    '<b>Sorry!</b> This user is disabled. Contact <a href="mailto:oleksandrzelentsov@gmail.com">'
                    'admin</a> to resolve this issue.')
            context = {'navigation_items': nav, 'username': request.POST['username'], 'errors': [msg]}
            return HttpResponse(get_template(template_name).render(context=context, request=request))
        else:
            # authorize if yes and redirect to main page
            auth_login(request, user)
            return HttpResponseRedirect('/')
        pass


def logout(request):
    if not isinstance(request.user, AnonymousUser):
        auth_logout(request)
    return HttpResponseRedirect('/')


def error(request: HttpRequest, message: str):
    return HttpResponse(get_template('bt_error.html').render(context={'message': message}, request=request))


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            nav = NavigationItem.get_navigation(request, 2)
            context = {'navigation_items': nav}
            return HttpResponse(get_template('bt_register.html').render(context=context, request=request))
    elif request.method == 'POST':
        # check parameters
        # collect errors
        # if there are any errors, return the same page with them
        # if everything is okay, check if the user with the same
        # email or username is present
        pass
    else:
        return error(request, '%s method is not allowed for this page' % request.method)
