from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template

from serverdict_db.settings import FORM_FIELD_CLASS
from ..models import Term
from ..my_library.charts import TermsCountByCategoryChart, TermsPopularityChart
from ..my_library.html_helper import NavigationItem, Alert


def error(request, message, redirect=None):
    nav = NavigationItem.get_navigation(request)
    current_user = request.user
    return HttpResponse(get_template('bt_error.html').render(
        context={'alert': Alert(message), 'redirect': redirect, 'navigation_items': nav,
                 'field_class': FORM_FIELD_CLASS, 'current_user': current_user, 'title': 'Error'}, request=request))


def success(request, message, redirect=None):
    nav = NavigationItem.get_navigation(request)
    current_user = request.user
    context = {'alert': Alert(message, 'success'),
               'navigation_items': nav, 'redirect': redirect,
               'field_class': FORM_FIELD_CLASS,
               'current_user': current_user,
               'title': 'Success'}
    return HttpResponse(get_template('bt_error.html').render(context=context,
                                                             request=request))


def index(request):
    return HttpResponseRedirect('/terms')


def statistics(request):
    template_name = 'bt_statistics.html'
    nav = NavigationItem.get_navigation(request, -1)
    current_user = request.user
    super_users = User.objects.filter(is_superuser__exact=True)
    chart_by_category = TermsCountByCategoryChart(Term.get_terms(request.user))
    plot_ = chart_by_category.get_plot()
    chart_popularity = TermsPopularityChart(Term.get_terms(request.user).filter(~Q(user__in=super_users)).distinct())
    plot_ += chart_popularity.get_plot()
    context = {'navigation_items': nav, 'current_user': current_user, 'plot': plot_}
    return HttpResponse(get_template(template_name).render(request=request, context=context))
