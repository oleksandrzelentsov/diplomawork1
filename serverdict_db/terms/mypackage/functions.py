from django.http import HttpResponseRedirect
import urllib.parse as urllib


def get_error_page(msg=''):
    return HttpResponseRedirect('/error?message=%s' % (urllib.quote_plus(msg)))
