__author__ = 'Alexander Zelentsov'

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

    def __init__(self, text, href, active=False):
        self.text, self.href, self.active = text, href, active


class Article:

    def __init__(self, title, content, additional_info="", href=""):
        self.title, self.href, self.content, self.additional_info = title, href, content, additional_info


class Message:
    def __init__(self, content):
        self.content = content
