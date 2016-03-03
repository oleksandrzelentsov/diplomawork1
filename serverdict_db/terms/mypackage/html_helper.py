__author__ = 'Alexander Zelentsov'
from django.contrib.auth.models import AnonymousUser

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

	def get_navigation(request, active_index=-1):
		nav = [NavigationItem('<span class="glyphicon glyphicon-home"></span> Home', '/terms')]
		if isinstance(request.user, AnonymousUser):
			nav += [NavigationItem('<span class="glyphicon glyphicon-user"></span> Log in', '/login/'), NavigationItem('<span class="glyphicon glyphicon-book"></span> Sign up', '/register/')]
		else:
			nav += [NavigationItem('<span class="glyphicon glyphicon-menu-left"></span> Log out', '/logout/'), NavigationItem('<span class="glyphicon glyphicon-plus"></span> Add term', '/terms/add')]
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

	def __init__(self, text, alert_type=0):
		self.text, self.type = text, alert_types[alert_type % len(alert_types)]

	def __str__(self):
		return self.text
