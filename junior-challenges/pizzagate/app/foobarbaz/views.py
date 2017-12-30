import base64
import lxml.etree
import traceback
import os

import django.contrib.auth.views as auth_views
from django.db import transaction
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import *

FLAG_PIZZA = 'Pizza itanimullI'

def get_user_pizzas(user):
    admin = User.objects.get(username='admin')
    return Pizza.objects.filter(user__in=[admin,user]).order_by("created_at")

def get_user_orders(user):
    return Order.objects.filter(user=user).order_by("created_at")

def get_illuminati(user):
    admin = User.objects.get(username='admin')
    return Illuminato.objects.filter(user__in=[admin,user]).order_by("?")


def require_auth(func):
    auth_xml = b'''<?xml version="1.0" encoding="UTF-8" ?>
            <users>
                <user>
                    <firstname>Bernd</firstname>
                    <lastname>Brot</lastname>
                    <login>bernd</login>
                    <password>berndberndbernd</password>
                    <role>inactive</role>
                </user>
                <user>
                    <firstname>Shia</firstname>
                    <lastname>TheOneANdOnly</lastname>
                    <login>sh1a</login>
                    <password>just_do_it_goddamnit</password>
                    <role>admin</role>
                </user>
            </users>
    '''

    def wrapper(req):
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm=devs_only'

        if 'HTTP_AUTHORIZATION' in req.META:
            auth = req.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == "basic":
                auth = base64.b64decode(auth[1]).split(b':')
                login, password = auth[0].decode(), b':'.join(auth[1:]).decode()
                root = lxml.etree.fromstring(auth_xml)
                xpath = '//users/user[login="{}" and password="{}"]'.format(login, password)
                try:
                    users = root.xpath(xpath) 
                except Exception as e:
                    response['WWW-Authenticate'] += ' err=Unexpected Exception: ' + str(e)
                    return response

                if len(users) > 0:
                    user = users[0]
                    login = user.find('login').text
                    role = user.find('role').text
                    if role == 'admin':
                        return func(req)
                    else:
                        response['WWW-Authenticate'] += ' err=Your username is \'{}\' and your role is \'{}\', but \'admin\' role required.'.format(login, role)
                else:
                    response['WWW-Authenticate'] += ' err=You provided invalid credentials.'

        return response
    return wrapper


def handle404(req):
    return HttpResponse("404 - not found")

@login_required
@require_auth
def create_pizza(req):
    if req.method == 'POST' and req.user.profile.role == 'dev':
        form = PizzaForm(req.POST)
        if form.is_valid():
            pizza = form.save(commit=False)
            if get_user_pizzas(req.user).filter(name=pizza.name).exists():
                messages.add_message(req, messages.ERROR,'A pizza with that name exists already!')
            else:
                pizza.user = req.user
                pizza.save()
                return redirect('list_pizza')
        return render(req, 'foobarbaz/pizza.html', dict(form=form))

    return render(req, 'foobarbaz/pizza.html', dict(form=PizzaForm()))

@login_required
@require_auth
def list_orders(req):
    orders = get_user_orders(req.user)
    return render(req, 'foobarbaz/orders.html', dict(orders=orders))

@require_auth
def list_pizzas(req):
    if req.user.is_authenticated:
        pizzas = get_user_pizzas(req.user)
    else:
        admin = User.objects.get(username='admin')
        pizzas = Pizza.objects.filter(user=admin).order_by('created_at')
    return render(req, 'foobarbaz/pizzas.html', dict(pizzas=pizzas))


@login_required
@require_auth
def create_order(req):
    if req.method == 'POST' and 'pizza' in req.POST:
        form = OrderForm(req.POST, user=req.user)
        pizza = req.POST.get('pizza')
        try:
            pizza = get_user_pizzas(req.user).get(name=pizza)
        except Pizza.DoesNotExist:
            return render(req, 'foobarbaz/order.html', dict(form=form))

        enough_balance = False
        with transaction.atomic():
            user_profile = req.user.profile
            if pizza.price <= user_profile.balance:
                user_profile.balance -= pizza.price
                user_profile.save()
                enough_balance = True
        if enough_balance:
                order = Order(user=req.user, pizza=pizza)
                order.save()
                if pizza.name == FLAG_PIZZA:
                    req.user.profile.is_illuminati = True
                    req.user.save()
                    return redirect('illuminati')
                return redirect('list_order')
        else:
            messages.add_message(req, messages.ERROR,'You can\'t afford that!')
            return render(req, 'foobarbaz/order.html', dict(form=form))

    form = OrderForm(user=req.user)
    return render(req, 'foobarbaz/order.html', dict(form=form))


@require_auth
def illuminati(req):
    if not req.user.is_authenticated or not req.user.profile.is_illuminati:
        return handle404(req)

    if req.method == 'POST':
        xml = req.POST.get('xml')
        if xml:
            try:
                root = lxml.etree.fromstring(xml)
                video_id = root.xpath('/illuminato/video') 
                details = root.xpath('/illuminato/details') 
                if video_id and details:
                    Illuminato.objects.create(details=details[0].text, 
                            video=video_id[0].text, 
                            user=req.user).save()
                else:
                    return HttpResponseServerError("<video> or <details> missing")
            except Exception as e:
                return HttpResponseServerError(str(e) + "\n" + xml)


            

    illuminati = get_illuminati(req.user)
    return render(req, 'foobarbaz/illuminati.html', dict(illuminati=illuminati))

@require_auth
def index(req):
    if req.user.is_authenticated and req.user.profile.is_illuminati:
            return redirect('illuminati')
        
    if req.method == 'POST':
        form = AuthenticationForm(data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(req, user)
            else:
                messages.add_message(req, messages.ERROR,'Invalid credentials!')
        else:
            for e in form.errors['__all__']:
                messages.add_message(req, messages.ERROR, e)

    return render(req, 'foobarbaz/index.html')

@require_auth
def signup(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            role = req.POST.get('role')
            if not role or role not in ['user', 'dev']:
                messages.add_message(req, messages.ERROR, 
                        'Invalid value \'{}\' for user role. Only \'user\' and \'dev\' supported.'.format(role))
            else:
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(req, user)
                user.profile.balance = 100
                user.profile.role = role
                user.save()
                return redirect('index')
    else:
        form = UserCreationForm()
    return render(req, 'foobarbaz/signup.html', {'form': form})


@require_auth
def do_logout(req):
    logout(req)
    return redirect("index")
