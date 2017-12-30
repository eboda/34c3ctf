from django.conf.urls import url, include
from django.contrib import admin
from django.shortcuts import redirect
from django.views.generic import TemplateView, RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import Http404

from . import views
import foobarbaz

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup$', views.signup,name='signup'),
    url(r'^logout$', views.do_logout,name='logout'),
    url(r'^order/list$', views.list_orders,name='list_order'),
    url(r'^order/create$', views.create_order,name='create_order'),
    url(r'^pizza/create$', views.create_pizza,name='create_pizza'),
    url(r'^pizza/list$', views.list_pizzas,name='list_pizza'),
    url(r'^illuminati$', views.illuminati,name='illuminati'),
    url(r'^.*$', views.handle404, name='catchall'),
]
urlpatterns += staticfiles_urlpatterns()
