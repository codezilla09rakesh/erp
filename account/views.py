from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.models import User
from account.form import RegisterForm, UserLogin, MyProfileForm
from django.contrib.auth import login, logout, authenticate
from account.models import MyProfile, CustomUser
from django.contrib.auth.decorators import login_required
from account.decorators import unauthenticated_user, is_manager
from holiday.models import YourEmployee, Leave
from django.contrib import messages

from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
@ login_required(login_url='login')
def home(req):
    if req.user.is_authenticated:
        user = req.user
        user = CustomUser.objects.get(username = user)
        # print('user',req.user.is_manager)
        if user.is_manager:
            your_employee = YourEmployee.objects.filter(manager=user)
        else:
            try:
                your_employee = YourEmployee.objects.get(employee=user)
            except:
                your_employee  = None

        taken_leave = Leave.objects.filter(employee = user, status='accepted').count()
        context = {'employee_list': your_employee, "taken_leave":taken_leave}
    else:
        context = {}
    return render(req, "accounts/index.html", context)

@unauthenticated_user
def register(req):
    if req.method == "POST":
        form = RegisterForm(req.POST)
        if form.is_valid():
            if req.POST.get("is_manager") == "on":
                var = True
            else:
                var = False
            user=CustomUser.objects.create_user(
                username=req.POST.get("username"),
                password=req.POST.get("password"),
                first_name=req.POST.get("first_name"),
                last_name=req.POST.get("last_name"),
                email=req.POST.get("username"),
                is_manager = var,
            )
            user.save()
            print('user',user)
            if var:
                manager = CustomUser.objects.get(username='admin')
                YourEmployee.objects.create(
                    manager=manager,
                    employee = user, )
            if user is not None:
                # Here login is set the user in session. Now we get whole info of user
                login(req, user)
                # print("user is logged in")
                return redirect('home')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(req, "accounts/register.html", context)

# @unauthenticated_user
def Userlogin(req):
    form = UserLogin()
    if req.method == "POST":
        form = UserLogin(req.POST)
        if form.is_valid():
            user = authenticate(username = req.POST.get('username'),password = req.POST.get('password'))
            if user is not None:
                login(req, user)
                return redirect('home')
            else:
                messages.info(req, 'Username or Password is incorrect ')
    context = {'form': form}
    return render(req, "accounts/login.html", context)


@ login_required(login_url='login')
def Addprofile(req):
    if req.method == "POST":
        form = MyProfileForm(req.POST, req.FILES)
        if form.is_valid():
            user = req.user
            user = CustomUser.objects.get(username = user)
            mobile = req.POST.get('mobile')
            gender = req.POST.get('gender')
            profile_pic = req.FILES.get('profile_pic')
            print('profile pic1 ',profile_pic)
            MyProfile.objects.create(user=user,
                                     mobile=mobile,
                                     gender=gender,
                                     profile_pic=profile_pic,)

            return redirect('profile')
        else:
            print(form.errors)
    else:
        form = MyProfileForm()
    context = {'form': form}
    return render(req, "accounts/profile.html", context)

@ login_required(login_url='login')
def Editprofile(req):
    user = req.user
    profile = MyProfile.objects.get(user = user)
    form = MyProfileForm(instance=profile)
    if req.method == "POST":

        # When will new file is upload then old file has deleted
        form = MyProfileForm(req.POST, req.FILES)
        if form.is_valid() and 'profile_pic' in req.FILES:
            profile.profile_pic.delete()

        form = MyProfileForm(req.POST, req.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print('show error', form.errors)
    context = {'form':form, 'pro':'edit'}
    return render(req, "accounts/edit_profile.html", context)

@ login_required(login_url='login')
def Profile(req):
    try:
        user = req.user
        profile = MyProfile.objects.get(user = user)
    except:
        return redirect('add_profile')
    context={'profile': profile}
    return render(req, "accounts/show_profile.html",    context)

@ login_required(login_url='login')
def Userlogout(req):
    if req.user.is_authenticated:
        logout(req)
        return redirect('login')

@is_manager
def AddEmployee(req):
    user = CustomUser.objects.filter(is_manager=False)
    employee = [i.employee for i in YourEmployee.objects.all()]
    user_list = [i for i in user if i not in employee]
    if req.method == "POST":
        manager = req.user
        for i in user:
            id = req.POST.get(str(i.id))
            if id:
                employee = CustomUser.objects.get(id = i.id)
                YourEmployee.objects.create(
                    manager = manager,
                    employee = employee,
                )
                return redirect('home')
            else:
                pass

    context = {'user':user_list}
    return render(req, "accounts/Add_employee.html", context)

@is_manager
def RemoveEmployee(req):
    user = req.user
    your_employee = YourEmployee.objects.filter(manager=user)
    if req.method == "POST":
        for employee in your_employee:
            id = req.POST.get(str(employee.id))
            # print('$$$$$$$$$$$$$$$$$$', id)
            if id:
                YourEmployee.objects.get(id = employee.id).delete()
                return redirect('home')
    context = {'user': your_employee}
    # context = {}
    return render(req, "accounts/remove_employee.html", context)
