from django.http import HttpResponseRedirect
from terms.mypackage import functions


def get(request, what):
    return functions.get_error_page('Api is not implemented yet! Sorry!')
