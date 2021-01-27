from django.shortcuts import render,redirect
from holiday.form import LeaveForm, ApprovedForm, ResionForm
from holiday.models import Leave, YourEmployee, Resions
from account.models import CustomUser
from django.contrib.auth.decorators import login_required

# from
# Create your views here.

@ login_required(login_url='login')
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
                starting_date = req.POST['starting_date'],
                ending_date=date,
                half_day=req.POST['half_day'],
            )
            return redirect('home')
    else:
        form = LeaveForm()
        print('form',form)
    context = {'form': form}
    return render(req, "leaves/leaves.html", context)

@ login_required(login_url='login')
def ListLeaves(req):
    user = CustomUser.objects.get(username = req.user)
    leave = Leave.objects.filter(employee=user)
    context = {"leaves": leave}
    return render(req, "leaves/show_leaves.html", context)

@ login_required(login_url='login')
def ShowLeave(req,id):
    leave = Leave.objects.get(id=id)
    context = {'leave':leave}
    return render(req,'leaves/leave_detail.html',context)

def ApprovedLeave(req,val):
    user = CustomUser.objects.get(username=req.user)
    leaves = Leave.objects.filter(manager = user, status='panding')
    if req.method == "POST":
        form = ApprovedForm(req.POST)
        if form.is_valid():
            leave = Leave.objects.get(id = int(val))
            leave.status = req.POST['status']
            leave.save()
            print('staus', req.POST['status'])
            if req.POST['status'].strip(" ") == "resion":
                return redirect('resion',int(val))
        else:
            print(form.errors)
        # for leave in leaves:
        #     type = req.POST.get(str(leave.id))
        #     if type:
        #         type = type.strip(" ").lower()
        #         if type == "approved":
        #             leave = Leave.objects.get(id = leave.id)
        #             leave.status = "approved"
        #             leave.save()
        #         elif type == "cancel":
        #             leave = Leave.objects.get(id=leave.id)
        #             leave.status = "resion"
        #             leave.save()
        #         else:
        #             print("else",type)
    else:
        form = ApprovedForm()
    # print('var = ',leaves[0].employee.first_name)
    context = {'leaves':leaves, 'form':form}
    return render(req, "leaves/approved_leave.html",context)

def ResionView(req,id):
    if req.method == "POST":
        form = ResionForm(req.POST)
        if form.is_valid():
            # manager = CustomUser.objects.get(username = req.user)
            leave = Leave.objects.get(id=id)
            employee = leave.employee
            Resions.objects.create(
                employee = employee,
                leave = leave,
                title = req.POST['title'],
                description = req.POST['description'],
            )
            return redirect('home')
    else:
        form = ResionForm()
    context = {'form': form, 'id': id}
    return render(req, "leaves/resion_form.html",context)

def ResionShow(req, id):
    reject = Resions.objects.get(leave= id)
    print('reject',reject)
    context = {'reject':reject}
    return render(req, 'leaves/resion_show.html', context)