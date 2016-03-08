from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.template.loader import get_template

from terms.models import Term
from terms.mypackage.html_helper import *
from serverdict_db.settings import ADMIN_EMAIL


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
    nav = NavigationItem.get_navigation(request, 1)
    if request.method == 'GET':
        return HttpResponse(get_template(template_name).render(context={'navigation_items': nav}, request=request))
    elif request.method == 'POST':
        # check data
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            # return the same page with errors if no
            alert1 = Alert('<b>Error!</b> Wrong authentication data.', 'danger')
            context = {'navigation_items': nav, 'username': request.POST['username'],
                       'errors': [alert1]}
            return HttpResponse(get_template(template_name).render(context=context, request=request))
        elif not user.is_active:
            msg = Alert(
                '<b>Sorry!</b> This user is disabled. Contact <a href="mailto:%s">' % ADMIN_EMAIL +
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


def error(request: HttpRequest, message: str, redirect=None):
    nav = NavigationItem.get_navigation(request)
    return HttpResponse(get_template('bt_error.html').render(
        context={'alert': Alert(message), 'redirect': redirect, 'navigation_items': nav},
        request=request))


def success(request: HttpRequest, message: str, redirect=None):
    nav = NavigationItem.get_navigation(request)
    return HttpResponse(get_template('bt_error.html').render(context={'alert': Alert(message, 'success'),
                                                                      'navigation_items': nav, 'redirect': redirect},
                                                             request=request))


def register(request):
    template_name = 'bt_register.html'
    nav = NavigationItem.get_navigation(request, 2)
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            context = {'navigation_items': nav}
            return HttpResponse(get_template(template_name).render(context=context, request=request))
    elif request.method == 'POST':
        # collect parameters
        errors = []
        form_data = request.POST

        def p(x):
            # print(x, ":", form_data[x])
            return form_data[x]

        username = p('username').strip()
        password = p('password')
        repeat_password = p('repeat_password')
        email = p('email').strip()
        first_name = p('first_name').strip()
        last_name = p('last_name').strip()

        # check parameters
        # necessary parameters:
        necessary_parameters = (username, password, repeat_password, email)
        if '' in necessary_parameters:
            errors.append(Alert('<b>Read carefully!</b> Some of necessary fields left empty.'))

        # password matching
        if password != repeat_password:
            errors.append(Alert('<b>Type carefully!</b> Passwords don\'t match.'))

        # check if the user with the same email or username is present
        if username in [x.username for x in User.objects.all()]:
            errors.append(Alert('<b>Username problem!</b> User with username "%s" already exists.' % username))

        if email in [x.email for x in User.objects.all()]:
            errors.append(Alert('<b>E-mail problem!</b> User with e-mail %s already exists.' % email))

        # if there are any errors, return the same page with them
        if errors:
            leftover = dict(form_data)
            leftover.update({'errors': errors, 'navigation_items': nav})
            leftover.update({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})
            # print(leftover)
            return HttpResponse(get_template(template_name).render(context=leftover, request=request))
        else:
            # return error(request, "Success creating user with parameters %s" % form_data)
            User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            return success(request, '<h3>Success</h3>creating user.', redirect={'url': '/', 'time': 5})
    else:
        return error(request, '%s method is not allowed for this page' % request.method)
