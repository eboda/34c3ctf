"""quaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.shortcuts import redirect
from django.views.generic import TemplateView, RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^feed$', views.feed, name='feed'),
    url(r'^feed/(?P<token>[^/]+)$', views.feed, name='feed'),
    url(r'^feed/(?P<token>[^/]+)/follow$', views.follow, name='follow'),
    url(r'^followers$', views.followers, name='followers'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^messages$', views.view_messages, name='messages'),
    url(r'^messages/new$', views.create_message, name='create_message'),
    url(r'^messages/(?P<token>[^/]+)$', views.view_message, name='view_message'),
    url(r'^messages/new/(?P<to_user>[^/]+)$', views.create_message, name='create_message'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^signup$', views.signup, name='signup'),
]
urlpatterns += staticfiles_urlpatterns()
