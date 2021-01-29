from django.shortcuts import redirect
from django.http import HttpResponse
from holiday.models import YourEmployee
from account.models import CustomUser

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def is_manager(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_manager:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("<p>This Page is only for manager</p> ")
    return wrapper_func

def manageravailable(view_func):
    def wrapper_func(request, *args, **kewargs):
        if request.user.is_manager != True:
            try:
                user = CustomUser.objects.get(username = request.user)
                get_manager = YourEmployee.objects.get(employee=user)
                print('get manager', get_manager)
                return view_func(request, *args, **kewargs)
            except YourEmployee.DoesNotExist:
                return HttpResponse("Currently you does not have any Manager.")
        else:
            return view_func(request, *args, *kewargs)
    return wrapper_func


