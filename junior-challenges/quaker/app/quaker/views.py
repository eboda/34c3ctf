import random
import re

import django.contrib.auth.views as auth_views
from django.db import transaction
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import *

admin_msg = """
    Welcome to Quaker!

    I hope you will enjoy this new app I built! It is super secure and respects your privacy!
    On this platform, no one can find you unless you want them to find you!

    I read regularly my new messages and watch new Quaks in my network! If you find a bug,
    write me a message!

    Cheers,
    admin.
"""

@login_required
def followers(req):
    followers = UserProfile.objects.filter(following__in=[req.user])
    return render(req, 'followers.html', dict(followers=followers))

def index(req):
    if req.user.is_authenticated:
        return redirect('feed')

    if req.method == 'POST':
        form = AuthenticationForm(data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=raw_password)
            if user is not None:
                auth.login(req, user)
            else:
                messages.add_message(req, messages.ERROR,'Invalid credentials!')
        else:
            for e in form.errors['__all__']:
                messages.add_message(req, messages.ERROR, e)
        return redirect('index')

    return render(req, 'index.html')

def get_user(token):
    return UserProfile.objects.filter(token=token)

@login_required
def view_message(req, token):
    msg = Message.objects.filter(token=token)
    if not msg.exists():
        messages.add_message(req, messages.ERROR, 'Message does not exist.')
        return redirect('messages')

    msg = msg.get()
    if msg.user_to != req.user and msg.user_from != req.user:
        messages.add_message(req, messages.ERROR, 'That is not your message!')
        return redirect('messages')

    if msg.user_to == req.user:
        msg.seen = True
        msg.save()

    return render(req, 'view_message.html', dict(msg=msg))



@login_required
def follow(req, token):
    if token:
        user = get_user(token)
        if not user.exists():
            messages.add_message(req, messages.ERROR, 'User does not exist.')
        else:
            req.user.profile.following.add(user.get().user)
            messages.add_message(req, messages.INFO, 'You are now following {}.'.format(user.get().user))

    return redirect('feed')


@login_required
def feed(req, token=''):
    story = req.POST.get('story')
    if story:
        t = Quak.objects.create(message=story)
        t.save()
        req.user.profile.quaks.add(t)
        req.user.save()
        return redirect('feed', token=req.user.profile.token)

    if token:
        profile = get_user(token)
        if not profile.exists():
            messages.add_message(req, messages.ERROR, 'User does not exist.')
            return redirect('feed')
        else:
            user = profile.get().user
            if user != req.user and user not in req.user.profile.following.all():
                return render(req, 'feed.html', dict(owner=user, notfollowing=True))
            else:
                return render(req, 'feed.html', dict(owner=user))

    return render(req, 'feed.html', dict(listfollowers=True, following=req.user.profile.following.all()))

def signup(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=username, password=raw_password)
            auth.login(req, user)
            user.profile.token = '{:x}'.format(random.SystemRandom().getrandbits(128))
            user.profile.profile_pic = '/static/img/profile1.png'
            user.save()

            admin = User.objects.filter(pk=1).get()
            token = '{:x}'.format(random.SystemRandom().getrandbits(140))
            Message.objects.create(user_from=admin, user_to=user, message=admin_msg, token=token).save()
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(req, 'signup.html', {'form': form})

def login(req):
    return HttpResponse("login")

@login_required
def logout(req):
    auth.logout(req)
    return redirect('index')

@login_required
def view_messages(req):
    received = Message.objects.filter(user_to=req.user)
    sent = Message.objects.filter(user_from=req.user)
    return render(req, 'messages.html', dict(msg_recv=received, msg_sent=sent))

@login_required
def create_message(req, to_user=''):
    if req.method == 'POST':
        token = req.POST.get('token')
        if token:
            return redirect('create_message', to_user=token)

        message = req.POST.get('message')
        to_user = get_user(to_user)
        if not to_user.exists():
            messages.add_message(req, messages.ERROR, 'User does not exist.')
            return redirect('create_message')

        if message:
            token = '{:x}'.format(random.SystemRandom().getrandbits(140))
            Message.objects.create(user_from=req.user, user_to=to_user.get().user, message=message, token=token).save()
            messages.add_message(req, messages.INFO, 'Message sent!')
            return redirect('messages')

    if to_user:
        recipient = get_user(to_user)
        if recipient.exists():
            return render(req, 'create_message.html', dict(to=recipient.get().user))
        else:
            messages.add_message(req, messages.ERROR, 'User does not exist.')
            return redirect('create_message')

    return render(req, 'create_message.html')

@login_required
def profile(req):
    if req.method == 'POST':
        profile_pic = req.POST.get('profile_pic')
        desc = req.POST.get('description')
        if req.user.pk != 1:    # don't allow profile updates to admin
            if profile_pic:
                if not profile_pic.endswith(".png"):
                    messages.add_message(req, messages.ERROR, 'Invalid profile pic. Must be a .png')
                else:
                    req.user.profile.profile_pic = profile_pic
                    req.user.save()
            if desc:
                req.user.profile.description = desc
                req.user.save()

            
            return redirect('profile')
        


    return render(req, "profile.html")
