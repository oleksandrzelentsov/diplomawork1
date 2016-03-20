from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template

from serverdict_db.settings import FORM_FIELD_CLASS
from terms.my_library.html_helper import NavigationItem
from terms.my_library.validation import LoginFormValidator, RegisterFormValidator
from terms.views.misc import success, error


def login(request):
    if not isinstance(request.user, AnonymousUser):
        return HttpResponseRedirect('/')
    template_name = 'bt_login_form.html'
    navigation_items = NavigationItem.get_navigation(request, 1)
    current_user = request.user
    context = {'navigation_items': navigation_items, 'field_class': FORM_FIELD_CLASS, 'current_user': current_user}
    if request.method == 'GET':
        return HttpResponse(
                get_template(template_name).render(
                        context=context,
                        request=request))
    elif request.method == 'POST':
        form_validator = LoginFormValidator(**dict(request.POST))
        errors = form_validator.errors()
        current_user = request.user
        if errors:
            # return the same page with errors if no
            context = {'navigation_items': navigation_items, 'username': form_validator.form_data()['username'],
                       'errors': errors, 'field_class': FORM_FIELD_CLASS, 'current_user': current_user}
            return HttpResponse(get_template(template_name).render(context=context, request=request))
        else:
            # authorize if yes and redirect to main page
            user = form_validator.form_data()['user']
            auth_login(request, user)
            return HttpResponseRedirect('/')
        pass


def logout(request):
    if not isinstance(request.user, AnonymousUser):
        auth_logout(request)
    return HttpResponseRedirect('/')


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
            return success(request, '<h3>Success</h3>creating user.', redirect={'url': '/', 'time': 3})
    else:
        return error(request, '%s method is not allowed for this page' % request.method)