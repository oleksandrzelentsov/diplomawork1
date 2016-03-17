from datetime import datetime

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template

from serverdict_db.settings import FORM_FIELD_CLASS
from terms.models import Term, Category, Author
from terms.mypackage.html_helper import *
from terms.mypackage.validation import RegisterFormValidator, LoginFormValidator, AddTermFormValidator


def index(request):
    return HttpResponseRedirect('/terms')


def search(request):
    nav = NavigationItem.get_navigation(request)
    current_user = request.user
    context = {'terms': Term.get_terms(request.user), 'navigation_items': nav, 'field_class': FORM_FIELD_CLASS,
               'current_user': current_user}
    if request.method == 'GET':
        name = request.GET.get('name')
        category = request.GET.get('category')
        if not (name or category):
            return HttpResponseRedirect('/')
        else:
            categories = Category.objects.all()
            context.update({'name': name, 'categories': categories})
            if name:
                context.update({'terms': Term.objects.filter(
                        Q(name__icontains=context['name'].lower()) | Q(definition__icontains=context['name'].lower()))})
            if category:
                context.update({'category': int(category)})
                context.update({'terms': context['terms'].filter(
                                    Q(category__exact=Category.objects.get(pk=context['category'])))})
        return HttpResponse(get_template('bt_search.html').render(context=context, request=request))
    else:
        return error(request, '%s method is not allowed for this page' % request.method)


def terms(request):
    nav = NavigationItem.get_navigation(request, 0)
    current_user = request.user
    context = {'terms': Term.get_terms(request.user), 'navigation_items': nav, 'field_class': FORM_FIELD_CLASS,
               'current_user': current_user}
    if request.method == 'GET':
        return HttpResponse(get_template("bt_terms.html").render(context=context, request=request))
    else:
        return error(request, '%s method is not allowed for this page' % request.method)


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


def error(request, message: str, redirect=None):
    nav = NavigationItem.get_navigation(request)
    current_user = request.user
    return HttpResponse(get_template('bt_error.html').render(
            context={'alert': Alert(message), 'redirect': redirect, 'navigation_items': nav,
                     'field_class': FORM_FIELD_CLASS, 'current_user': current_user, 'title': 'Error'},
            request=request))


def success(request, message: str, redirect=None):
    nav = NavigationItem.get_navigation(request)
    current_user = request.user
    context = {'alert': Alert(message, 'success'),
               'navigation_items': nav, 'redirect': redirect,
               'field_class': FORM_FIELD_CLASS,
               'current_user': current_user,
               'title': 'Success'}
    return HttpResponse(get_template('bt_error.html').render(context=context,
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
            return success(request, '<h3>Success</h3>creating user.', redirect={'url': '/', 'time': 3})
    else:
        return error(request, '%s method is not allowed for this page' % request.method)


@login_required(login_url='/login/')
def add_term(request):
    template_name = 'bt_add_term.html'
    nav = NavigationItem.get_navigation(request, 2)
    current_user = request.user
    categories = sorted(Category.objects.all(), key=lambda x: x.name)
    authors = list(sorted(Author.objects.all(), key=lambda x: x.name))
    special_authors = list(filter(lambda x: 'author' in x.name.lower(), authors))
    for i in special_authors:
        authors.remove(i)
    years = Year.get_years()
    context = {'navigation_items': nav, 'categories': categories, 'years': years, 'field_class': FORM_FIELD_CLASS,
               'current_user': current_user, 'authors': authors, 'special_authors': special_authors}
    if request.method == 'GET':
        return HttpResponse(get_template(template_name).render(context=context, request=request))
    elif request.method == 'POST':
        form_validator = AddTermFormValidator(**dict(request.POST))
        errors = form_validator.errors()
        if errors:
            context.update({'errors': errors})
            return HttpResponse(get_template(template_name).render(context=context, request=request))
        else:
            new_term = Term.objects.create(date_added=datetime.now(), user=current_user, **form_validator.form_data())
            if current_user.is_superuser:
                new_term.public = True
            else:
                new_term.accessibility.add(current_user)
            new_term.save()
            return success(request, '<h3>Success</h3>creating term.', redirect={'url': '/', 'time': 3})
    else:
        return error(request, '%s method is not allowed for this page' % request.method)


def term(request, term_id):
    template_name = 'bt_term.html'
    nav = NavigationItem.get_navigation(request)
    current_user = request.user
    if request.method == 'GET':
        term_ = Term.objects.get(pk=term_id)
        if term_:
            if term_.is_accessible(request.user):
                if term_.year:
                    print(term_.year)
                    term_.year = Year.get_string_by_value(term_.year)
                context = {'navigation_items': nav, 'term': term_, 'current_user': current_user}
                return HttpResponse(get_template(template_name).render(context=context, request=request))
            else:
                return error(request, 'Sorry, you don\'t have access to this page')
        else:
            return error(request, 'no such term with id %i' % term_id)
    else:
        return error(request, '%s method is not allowed for this page' % request.method)


def delete_term(request, term_id):
    template_name = 'bt_term_deletion.html'
    term_ = Term.objects.get(pk=term_id)
    if request.method == 'GET':
        if not term_:
            return error(request, 'Sorry, this page does not exist.')
        if request.user.is_superuser or request.user == term_.user:
            navigation_items = NavigationItem.get_navigation(request)
            context = {'navigation_items': navigation_items, 'term': term_, 'current_user': request.user}
            return HttpResponse(get_template(template_name).render(request=request, context=context))
    elif request.method == 'POST':
        if term_:
            term_.delete()
            return success(request, 'You have deleted your term!', {'time': 3, 'url': '/'})


def statistics(request):
    template_name = 'bt_statistics.html'
    nav = NavigationItem.get_navigation(request)
    current_user = request.user
    plot = Charts.get_test()
    context = {'navigation_items': nav, 'current_user': current_user, 'plot': plot}
    return HttpResponse(get_template(template_name).render(request=request, context=context))