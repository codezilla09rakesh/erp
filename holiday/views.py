from django.shortcuts import render,redirect
from holiday.form import LeaveForm
from holiday.models import Leave, YourEmployee
from account.models import CustomUser
# from
# Create your views here.

def AddLeave(req):
    user = CustomUser.objects.get(username= req.user)
    print('user', user)
    try:
        manager = YourEmployee.objects.get(employee = user)
        manager = CustomUser.objects.get(username=manager.manager.username)
    except:
        manager = None
    # print('manager', type(manager))
    if req.method == "POST":
        form = LeaveForm(req.POST)
        if form.is_valid():
            if req.POST['ending_date']:
                date = req.POST['ending_date']
            else:
                date = None
            Leave.objects.create(
                manager = manager,
                employee = user,
                title= req.POST['title'],
                description=req.POST['description'],
                ending_date=date,
                half_day=req.POST['half_day'],
            )
            return redirect('home')
    else:
        form = LeaveForm()
    context = {'form': form}
    return render(req, "leaves/leaves.html", context)

def ListLeaves(req):
    user = CustomUser.objects.get(username = req.user)
    print(type(user), user)
    leave = Leave.objects.filter(employee=user)
    print('lear', leave)
    context = {}
    return render(req, "leaves/show_leaves.html", context)
