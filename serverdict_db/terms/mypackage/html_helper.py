from datetime import datetime

from django.contrib.auth.models import AnonymousUser
from math import ceil
from plotly import offline
import random

from terms.models import Category

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
    def get_navigation(request, active_index=None):
        nav = [NavigationItem('<span class="glyphicon glyphicon-home"></span> Home', '/terms')]
        if isinstance(request.user, AnonymousUser):
            nav += [NavigationItem('<span class="glyphicon glyphicon-user"></span> Log in', '/login/'),
                    NavigationItem('<span class="glyphicon glyphicon-book"></span> Sign up', '/register/')]
        else:
            nav += [NavigationItem('<span class="glyphicon glyphicon-menu-left"></span> Log out', '/logout/'),
                    NavigationItem('<span class="glyphicon glyphicon-plus"></span> Add term', '/terms/add')]
            if request.user.is_staff:
                nav += [NavigationItem('<span class="glyphicon glyphicon-wrench"></span> Administration', '/admin')]
        nav += [NavigationItem('<span class="glyphicon glyphicon-stats"></span> Statistics', '/statistics/')]
        if active_index:
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

    @staticmethod
    def get_years():
        years = [Year(int(-x * 1e+3), '%.1f hundred years BC' % x) for x in
                 list([y * 0.5 for y in range(1, 22)])[::-1]]
        years += [Year(x, str(x)) for x in (list(range(datetime.now().year + 1)))]
        years = years[::-1]
        years = [Year('', 'Unknown')] + years
        return years

    @staticmethod
    def get_string_by_value(value):
        years = Year.get_years()
        str_ = [x for x in years if x.numeric == value][0]
        return str_

    @staticmethod
    def get_value_by_string(str_):
        years = Year.get_years()
        value = [x for x in years if str(x) == str_][0]
        return value


class Pager:
    def __init__(self, *objects, split_number=7, page_number=0):
        self.page_number = page_number
        self.split_number = split_number
        self.objects = objects

    def __len__(self):
        return ceil(len(self.objects) / self.split_number)

    def current_page(self):
        return self[self.page_number]

    def __getitem__(self, index):
        if len(self) >= index >= 0:
            if index != len(self) - 1:
                return self.objects[(index * self.split_number):((index + 1) * self.split_number)]
            else:
                return self.objects[(index * self.split_number):]
        else:
            return self[(len(self) + index) % len(self)]


class TermsPagePager(Pager):
    def __init__(self, *objects, split_number=7, page_number=0, previous_url=None, next_url=None, current_url=None):
        super().__init__(*objects, split_number=split_number, page_number=page_number)
        if not previous_url:
            previous_url = '/terms/?page=%i' % (page_number - 1)
        if not next_url:
            next_url = '/terms/?page=%i' % (page_number + 1)
        if not current_url:
            current_url = '/terms/?page=%i' % page_number
        self.urls = {'previous': previous_url, 'next': next_url, 'current': current_url}


class Charts:
    default_args = {'auto_open': False, 'output_type': 'div', 'show_link': False}

    @staticmethod
    def get_terms_count_by_category(terms):
        import time
        all_cats_query_time_begin = time.time()
        all_categories = Category.objects.all()
        all_cats_query_time_end = time.time()
        print("all cats query time:", all_cats_query_time_end - all_cats_query_time_begin)
        data_creation_begin = time.time()
        data = [(cat, len(terms.filter(category__exact=cat))) for cat in all_categories]
        data_creation_end = time.time()
        print('data creation time:', data_creation_end - data_creation_begin)
        data_sorting_begin = time.time()
        data.sort(key=lambda x: str(x[0]))
        data_sorting_end = time.time()
        print('data sorting time:', data_sorting_end - data_sorting_begin)
        plot_begin = time.time()
        plot_ = offline.plot({
            "data": [
                {
                    'labels': [str(a[0]) for a in data],
                    'values': [a[1] for a in data],
                    'type': 'pie'
                }
            ],
            "layout": {
                'title': "Terms count by category"
            }
        }, **Charts.default_args)
        plot_end = time.time()
        print('plot time:', plot_end - plot_begin)
        return plot_

    @staticmethod
    def get_test():
        def my_range(first, last=None, step=1.0):
            if last is None:
                last = first
                first = 0
            i = first
            while i < last:
                yield i
                i += step

        x = list(my_range(-10, 10, 1e-3))

        return offline.plot({
            "data": [
                {
                    'x': x,
                    'y': list(map(lambda arg: arg ** 3, x))
                }
            ],
            "layout": {
                'title': "hello world"
            }
        }, **Charts.default_args)
