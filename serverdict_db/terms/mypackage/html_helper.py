from django.contrib.auth.models import AnonymousUser
import random

magic_words = ['Ugh', 'Shucks', 'Damn', 'Oh', 'Dammit', 'Heck', 'Oh my gosh', 'Holy cow', 'Whoa', 'Whaat?']
random.shuffle(magic_words)
current_index = 0


def get_random_magic_word():
    global current_index
    current_index += 1
    return magic_words[(current_index - 1) % len(magic_words)]


class NavigationItem:
    def __init__(self, text, href, active=False):
        self.text, self.href, self.active = text, href, active

    @staticmethod
    def get_navigation(request, active_index=-1):
        nav = [NavigationItem('<span class="glyphicon glyphicon-home"></span> Home', '/terms')]
        if isinstance(request.user, AnonymousUser):
            nav += [NavigationItem('<span class="glyphicon glyphicon-user"></span> Log in', '/login/'),
                    NavigationItem('<span class="glyphicon glyphicon-book"></span> Sign up', '/register/')]
        else:
            nav += [NavigationItem('<span class="glyphicon glyphicon-menu-left"></span> Log out', '/logout/'),
                    NavigationItem('<span class="glyphicon glyphicon-plus"></span> Add term', '/terms/add')]
            if request.user.is_staff:
                nav += [NavigationItem('<span class="glyphicon glyphicon-wrench"></span> Administration', '/admin')]

        if 0 <= active_index < len(nav):
            nav[active_index].active = True
        return nav


class Article:
    def __init__(self, title, content, additional_info="", href=""):
        self.title, self.href, self.content, self.additional_info = title, href, content, additional_info


class Alert:
    alert_types = ['success', 'info', 'warning', 'danger']

    def __init__(self, text, alert_type='danger'):
        self.text = text
        if isinstance(alert_type, int):
            self.alert_type = Alert.alert_types[alert_type]
        elif isinstance(alert_type, str) and alert_type in Alert.alert_types:
            self.alert_type = alert_type
        else:
            print("bad argument for Alert constructor: (%s: %s)" % (alert_type, alert_type.__class__.__name__))
            self.alert_type = 'danger'

    def __str__(self):
        return self.text


class Year:
    def __init__(self, numeric, string_representation):
        self.string_representation = string_representation
        self.numeric = numeric

    def __str__(self):
        return self.string_representation
