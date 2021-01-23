from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from account.form import RegisterForm, UserLogin, MyProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def home(req):

    return render(req, "accounts/index.html", )

def register(req):
    if req.method == "POST":
        form = RegisterForm(req.POST)
        if form.is_valid():
            user=User.objects.create_user(
                username=req.POST.get("username"),
                password=req.POST.get("password"),
                first_name=req.POST.get("first_name"),
                last_name=req.POST.get("last_name"),
                email=req.POST.get("username"),
            )
            user.save()
            if user is not None:
                # Here login is set the user in session. Now we get whole info of user
                login(req, user)
                print("user is logged in")
                return redirect('profile')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(req, "accounts/register.html", context)

def Userlogin(req):
    form = UserLogin()
    context = {'form': form}
    return render(req, "accounts/login.html", context)

def profile(req):
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",req.user)
    if req.method == "POST":
        form = MyProfileForm(req.POST, req.FILES)
        if form.is_valid():
            user = req.user
            mobile = req.POST.get('mobile')
            gender = req.POST.get('gender')
            manager = req.POST.get('manager')
            profile_pic = req.FILE.get('profile_pic')
            MyProfile.objects.create(user=user,
                                     mobile=mobile,
                                     gender=)
        else:
            print(form.errors)
    else:
        form = MyProfileForm()
    context = {'form': form}
    return render(req, "accounts/profile.html", context)