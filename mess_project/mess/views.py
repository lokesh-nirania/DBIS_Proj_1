from django.shortcuts import render, redirect
from mess.models import *
from users.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.

feedbacks = feedback.objects.all()
students = student.objects.all()

data = {
    'feedbacks' : feedbacks,
    'students' : students,
    'staffs' : staff.objects.all(),
    'inventory' : inventory.objects.all(),
    'suppliers' : supplier.objects.all(),
    'bills' : bill.objects.all(),
    'purchases' : purchase.objects.all(),
    'consumptions' : consumption.objects.all(),
    'expenses' : expenses.objects.all()

}


def home(request):
    if request.user.is_authenticated:
        if manager.objects.filter(user=request.user).exists():
            return render(request,'mess/manager_home.html',data)
    return render(request,'mess/home.html',{'feedbacks':feedbacks,'students':students, 'flag' : request.user.is_authenticated})

def about(request):
    return render(request,'mess/about.html')

@login_required
def reg_stu(request):
    if request.user.is_authenticated:
        if manager.objects.filter(user=request.user).exists():
            return render(request,'mess/registered_student_list.html',data)
        else:
            return HttpResponseForbidden()

@login_required
def reg_staff(request):
    if request.user.is_authenticated:
        if manager.objects.filter(user=request.user).exists():
            return render(request,'mess/registered_staff_list.html',data)
        else:
            return HttpResponseForbidden()