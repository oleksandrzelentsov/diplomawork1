from abc import abstractmethod
from django.template.loader import get_template
from django.template import Context, RequestContext
from .html_helper import NavigationItem
from django.http import HttpResponse


class RenderMethod:

    def __init__(self, template_name, request=None, **context_args):
        self.template_name = template_name
        if request is None:
            self.context = Context(context_args)
        else:
            self.context = RequestContext(request, context_args)

    def render(self):
        return HttpResponse(get_template(self.template_name).render(self.context))


class BasicPageMethod(RenderMethod):

    def __init__(self, request, main_content, sidebars, navigation_active_item=-1):
        RenderMethod.__init__(self, 'index.html', request, Navigation=NavigationItem.make_navigation(request, navigation_active_item), Content=main_content, Sidebars=sidebars)


class FormPageMethod(RenderMethod):

    def __init__(self, request, template_name, navigation_active_item=-1):
        RenderMethod.__init__(self, template_name, request, Navigation=NavigationItem.make_navigation(request, navigation_active_item))
