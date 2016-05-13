"""serverdict_db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from terms.views import misc, terms, auth

urlpatterns = [
    url(r'^$', misc.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^customadmin/', terms.custom_admin),
    url(r'^terms/$', terms.terms),
    url(r'^search/', terms.search),
    url(r'^terms/add/$', terms.add_term),
    url(r'^terms/([0-9]+)/$', terms.view_term),
    url(r'^terms/([0-9]+)/delete/$', terms.delete_term),
    url(r'^terms/([0-9]+)/edit/$', terms.edit_term),
    url(r'^terms/([0-9]+)/confirm/$', terms.confirm_term),
    url(r'^logout/$', auth.logout),
    url(r'^login/$', auth.login),
    url(r'^register/$', auth.register),
    url(r'^statistics/$', misc.statistics)

    # REST API:
    # url(r'^api/get/([a-zA-Z_][a-zA-Z0-9]*)', api.get),
]
