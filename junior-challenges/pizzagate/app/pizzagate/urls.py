"""pizzagate URL Configuration

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
import foobarbaz

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin', RedirectView.as_view(url='/')),
    url(r'^robots.txt$', TemplateView.as_view(template_name='pizzagate/robots.txt', content_type='text/plain')),
    url(r'^foobarbaz/', include('foobarbaz.urls'), name='foobarbaz')
    # url(r'^admin/', admin.site.urls),
]
urlpatterns += staticfiles_urlpatterns()
