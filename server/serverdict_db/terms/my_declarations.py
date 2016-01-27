__author__ = 'Alexander Zelentsov'
import random
from django.template.loader import get_template
from django.template import Context

lipsum = ["Lorem ipsum dolor sit amet,"
          " consectetur adipiscing elit."
          " Suspendisse pellentesque,"
          " ligula in faucibus ultricies,"
          " nulla velit euismod ex,"
          " non venenatis ligula purus dictum ex.",
          " Vivamus quis arcu tempus ante scelerisque pretium."
          " Pellentesque et odio iaculis, interdum libero non,"
          " gravida quam. Suspendisse auctor purus vitae sapien cursus aliquet.",
          " Vestibulum a odio vitae arcu finibus condimentum eget vitae mauris."
          " Aenean nec tempor velit. In quis dictum turpis.",
          " Quisque sodales at neque a laoreet."
          " Suspendisse mollis mattis justo,"
          " vitae suscipit lacus luctus vel.",
          " Nulla sit amet congue arcu."
          " Aenean at leo ut urna dictum volutpat sed eget neque."
          " Etiam fringilla libero eu justo convallis interdum.",
          " Donec massa libero, euismod sit amet sem id,"
          " malesuada congue eros. Mauris malesuada commodo libero at finibus.",
          " Aenean mattis volutpat lorem, nec gravida tellus cursus nec."
          " Class aptent taciti sociosqu ad litora torquent per conubia nostra,"
          " per inceptos himenaeos. Donec eget urna id urna porta consectetur vel sed. "]


class NavigationItem:

    def __init__(self, text, active="",  href="#"):
        self.text, self.href, self.active = text, href, active

    def get_html(self):
        return get_template("navigation_item.html").render(Context({"item": self}, autoescape=False))

    @staticmethod
    def get_html_for_menu(items):
        return get_template("navigation_items.html").render(Context({
            "navigation_items": [x.get_html for x in items]
        }, autoescape=False))


class Article:

    def __init__(self, title="", content="", additional_info="", href="#"):
        self.title, self.href, self.content, self.additional_info = title, href, content, additional_info

    def get_html(self):
        return get_template("article.html").render(Context({"article": self}, autoescape=False))


class Sidebar:

    def __init__(self, title, content, sidebar_type="middle-sidebar"):
        self.title, self.content, self.sidebar_type = title, content, sidebar_type

    def get_html(self):
        return get_template("sidebar.html").render(Context({"sidebar": self}, autoescape=False))


class Message:
    def __init__(self, content):
        self.content = content

    def get_html(self):
        return get_template("message.html").render(Context({"message": self}, autoescape=False))