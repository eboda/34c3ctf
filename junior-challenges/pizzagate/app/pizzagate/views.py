from django.http import HttpResponse
from django.shortcuts import redirect, render

def index(req):
    return render(req, 'pizzagate/index.html')

def admin(req):
    return redirect(req, '/')

def foobar_index(req):
    return HttpResponse("Your foobar:")
