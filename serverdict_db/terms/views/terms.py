from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template

from serverdict_db.settings import FORM_FIELD_CLASS
from ..models import Term, Category, Author
from ..my_library.html_helper import NavigationItem, Year
from ..my_library.pagers import TermsPagePager
from ..my_library.validation import AddTermFormValidator, EditTermFormValidator
from ..views.misc import error, success


def search(request):
    # TODO create filters of "my terms", "user-defined terms" and "Voter choice terms"
    nav = NavigationItem.get_navigation(request)
    current_user = request.user
    context = {'terms': Term.get_terms(request.user).distinct(), 'navigation_items': nav,
               'field_class': FORM_FIELD_CLASS,
               'current_user': current_user}
    if request.method == 'GET':
        name = request.GET.get('name')
        category = request.GET.get('category')
        if not (name or category):
            return HttpResponseRedirect('/')
        else:
            categories = Category.objects.all()
            context.update({'categories': categories})
            if name:
                context.update({'name': name})
                context.update({'terms': context['terms'].filter(
                        Q(name__icontains=context['name'].lower()) | Q(definition__icontains=context['name'].lower()))})
            if category:
                context.update({'category': int(category)})
                context.update({'terms': context['terms'].filter(
                        Q(category__exact=Category.objects.get(pk=context['category'])))})
            context.update({'terms': context['terms'].filter(
                    (Q(public__exact=True) | Q(accessibility__in=[current_user.id])))})
        return HttpResponse(get_template('bt_search.html').render(context=context, request=request))
    else:
        return error(request, '%s method is not allowed for this page' % request.method)


def terms(request):
    nav = NavigationItem.get_navigation(request, 0)
    current_user = request.user
    context = {'navigation_items': nav, 'field_class': FORM_FIELD_CLASS,
               'current_user': current_user}
    if request.method == 'GET':
        terms_ = Term.get_terms(current_user).order_by('-date_added').distinct()
        page_number = None
        if request.GET.get('page'):
            try:
                page_number = int(request.GET.get('page'))
            except ValueError:
                page_number = 0
                print('failed setting page number')
        pager = TermsPagePager(terms_, page_number=page_number if page_number else 0)
        context.update({'terms': pager.current_page(), 'pager': pager})
        return HttpResponse(get_template("bt_terms.html").render(context=context, request=request))
    else:
        return error(request, '%s method is not allowed for this page' % request.method)


@login_required(login_url='/login/')
def edit_term(request, term_id):
    term_to_edit = Term.objects.get(pk=term_id)
    if not term_to_edit:
        return error(request, 'term not found')
    template_name = 'bt_edit_term.html'
    nav = NavigationItem.get_navigation(request, 2)
    current_user = request.user
    categories = Category.objects.all()
    authors = Author.objects.filter(~Q(name__icontains='author')).order_by("name")
    special_authors = authors.filter(name__icontains='author')
    years = Year.get_years()
    context = {'navigation_items': nav, 'categories': categories, 'years': years, 'field_class': FORM_FIELD_CLASS,
               'current_user': current_user, 'authors': authors, 'special_authors': special_authors,
               'term': term_to_edit}
    if request.method == 'GET':
        return HttpResponse(get_template(template_name).render(context=context, request=request))
    elif request.method == 'POST':
        form_validator = EditTermFormValidator(dict(request.POST))
        errors = form_validator.errors()
        if errors:
            context.update({'errors': errors})
            return HttpResponse(get_template(template_name).render(context=context, request=request))
        else:
            author = form_validator.form_data()['author']
            if author:
                term_to_edit.author = author
            elif author == '':
                term_to_edit.author = None
            term_to_edit.category = form_validator.form_data()['category']
            term_to_edit.name = form_validator.form_data()['name']
            term_to_edit.definition = form_validator.form_data()['definition']
            term_to_edit.reset_term()
            term_to_edit.save()
            return success(request,
                           '<h3>Success</h3>editing term "%s".<br>Page will redirect in 3 seconds.' % term_to_edit,
                           redirect={'url': '/terms/%s/' % term_to_edit.id, 'time': 3})


@login_required(login_url='/login/')
def add_term(request):
    template_name = 'bt_add_term.html'
    nav = NavigationItem.get_navigation(request, 2)
    current_user = request.user
    categories = Category.objects.all()
    authors = Author.objects.filter(~Q(name__icontains='author')).order_by("name")
    special_authors = authors.filter(name__icontains='author')
    years = Year.get_years()
    context = {'navigation_items': nav, 'categories': categories, 'years': years, 'field_class': FORM_FIELD_CLASS,
               'current_user': current_user, 'authors': authors, 'special_authors': special_authors}
    if request.method == 'GET':
        return HttpResponse(get_template(template_name).render(context=context, request=request))
    elif request.method == 'POST':
        form_validator = AddTermFormValidator(dict(request.POST))
        errors = form_validator.errors()
        if errors:
            context.update({'errors': errors})
            return HttpResponse(get_template(template_name).render(context=context, request=request))
        else:
            forbidden_users = User.objects.filter(Q(is_superuser__exact=True) | Q(id__exact=request.user.id)).distinct()
            similar_terms = Term.objects.filter((Q(name__icontains=form_validator.form_data()['name']) | Q(
                    definition__icontains=form_validator.form_data()['name'])) & ~Q(
                user__in=forbidden_users)).distinct()
            if not similar_terms or request.POST.get('confirm'):
                new_term = Term.objects.create(date_added=datetime.now(), user=current_user,
                                               **form_validator.form_data())
                if current_user.is_superuser:
                    new_term.public = True
                else:
                    new_term.accessibility.add(current_user)
                new_term.save()
                Term.recalculate_publicity()
                return success(request, '<h3>Success</h3>creating term.<br>Page will redirect in 3 seconds.',
                               redirect={'url': '/', 'time': 3})
            else:
                # template_name = "confirmation.html"
                context.update({'terms': similar_terms})
                context.update(form_validator.form_data())
                return HttpResponse(get_template(template_name).render(context=context, request=request))
    else:
        return error(request, '%s method is not allowed for this page' % request.method)


def view_term(request, term_id):
    template_name = 'bt_term.html'
    nav = NavigationItem.get_navigation(request)
    current_user = request.user
    if request.method == 'GET':
        term_ = Term.objects.get(pk=term_id)
        if term_:
            if term_.is_accessible(request.user):
                if term_.year:
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
            Term.recalculate_publicity()
            return success(request, 'You have deleted your term!', {'time': 3, 'url': '/'})


@login_required(login_url='/login/')
def confirm_term(request, term_id):
    if request.method == 'POST':
        term_ = Term.objects.get(pk=term_id)
        if not term_:
            return error(request, '<h3>No such term with id=%i!</h3>' % term_id)
        term_.grant_access(request.user)
        return success(request, 'Term successfully confirmed!', redirect={'url': '/terms/%s/' % term_id, 'time': 3})
    else:
        return error(request, '%s method is not allowed for this page' % request.method)
