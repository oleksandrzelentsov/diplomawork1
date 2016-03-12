from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.template.loader import get_template

from serverdict_db.settings import ADMIN_EMAIL, FORM_FIELD_CLASS
from terms.models import Term, Category
from terms.mypackage.html_helper import *
from terms.mypackage.validation import RegisterFormValidator


def index(request):
    return HttpResponseRedirect('/terms')


def terms(request):
    if request.method == 'GET':
        nav = NavigationItem.get_navigation(request, 0)
        c_dict = {'terms': Term.get_terms(request.user), 'navigation_items': nav, 'field_class': FORM_FIELD_CLASS}
        return HttpResponse(get_template("bt_terms.html").render(context=c_dict, request=request))
    else:
        return error(request, '%s method is not allowed for this page' % request.method)


def login(request):
    if not isinstance(request.user, AnonymousUser):
        return HttpResponseRedirect('/')
    template_name = 'bt_login_form.html'
    nav = NavigationItem.get_navigation(request, 1)
    if request.method == 'GET':
        return HttpResponse(
            get_template(template_name).render(context={'navigation_items': nav, 'field_class': FORM_FIELD_CLASS},
                                               request=request))
    elif request.method == 'POST':
        # check data
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            # return the same page with errors if no
            alert1 = Alert('<b>Error!</b> Wrong authentication data.', 'danger')
            context = {'navigation_items': nav, 'username': request.POST['username'],
                       'errors': [alert1], 'field_class': FORM_FIELD_CLASS}
            return HttpResponse(get_template(template_name).render(context=context, request=request))
        elif not user.is_active:
            msg = Alert(
                    '<b>Sorry!</b> This user is disabled. Contact <a href="mailto:%s">' % ADMIN_EMAIL +
                    'admin</a> to resolve this issue.')
            context = {'navigation_items': nav, 'username': request.POST['username'], 'errors': [msg],
                       'field_class': FORM_FIELD_CLASS}
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


def error(request: HttpRequest, message: str, redirect=None):
    nav = NavigationItem.get_navigation(request)
    return HttpResponse(get_template('bt_error.html').render(
            context={'alert': Alert(message), 'redirect': redirect, 'navigation_items': nav,
                     'field_class': FORM_FIELD_CLASS},
            request=request))


def success(request: HttpRequest, message: str, redirect=None):
    nav = NavigationItem.get_navigation(request)
    return HttpResponse(get_template('bt_error.html').render(context={'alert': Alert(message, 'success'),
                                                                      'navigation_items': nav, 'redirect': redirect,
                                                                      'field_class': FORM_FIELD_CLASS},
                                                             request=request))


def register(request):
    template_name = 'bt_register.html'
    nav = NavigationItem.get_navigation(request, 2)
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            context = {'navigation_items': nav, 'field_class': FORM_FIELD_CLASS}
            return HttpResponse(get_template(template_name).render(context=context, request=request))
    elif request.method == 'POST':
        # collect parameters
        form_data = dict(request.POST)
        # validate
        form_validator = RegisterFormValidator(**form_data)
        # get errors
        errors = form_validator.errors()
        # if there are any errors, return the same page with them
        if errors:
            leftover = dict(form_validator.form_data())
            leftover.update({'errors': errors, 'navigation_items': nav, 'field_class': FORM_FIELD_CLASS})
            return HttpResponse(get_template(template_name).render(context=leftover, request=request))
        else:
            User.objects.create_user(**form_validator.form_data())
            return success(request, '<h3>Success</h3>creating user.', redirect={'url': '/', 'time': 5})
    else:
        return error(request, '%s method is not allowed for this page' % request.method)


@login_required(login_url='/login/')
def add_term(request):
    template_name = 'bt_add_term.html'
    nav = NavigationItem.get_navigation(request, 2)
    if request.method == 'GET':
        categories = Category.objects.all()
        years = [x + ' hundred years BC' for x in list(map(str, list([y * 0.5 for y in range(1, 22)])[::-1]))]
        years += (list(map(str, range(datetime.now().year + 1))))
        years = years[::-1]
        context = {'navigation_items': nav, 'categories': categories, 'years': years, 'field_class': FORM_FIELD_CLASS}
        return HttpResponse(get_template(template_name).render(context=context, request=request))
    elif request.method == 'POST':
        pass
    else:
        return error(request, '%s method is not allowed for this page' % request.method)
