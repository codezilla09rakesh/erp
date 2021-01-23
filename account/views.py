from django.shortcuts import render
from account.form import RegisterForm, UserLogin
from django.http import HttpResponse

# Create your views here.
def home(req):

    return render(req, "accounts/index.html", )

def register(req):
    form = RegisterForm()
    context = {'form': form}
    return render(req, "accounts/register.html", context)

def login(req):
    form = UserLogin()
    context = {'form': form}
    return render(req, "accounts/login.html", context)

def profile(req):
    context = {}
    return render(req, "accounts/profile.html", context)