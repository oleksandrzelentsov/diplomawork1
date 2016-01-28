from django.http import HttpResponseRedirect
from terms import my_declarations


def get(request, what):
    return my_declarations.get_error_page('Api is not implemented yet! Sorry!')
