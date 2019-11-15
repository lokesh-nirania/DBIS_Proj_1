from django.shortcuts import render, redirect
from mess.models import *
from users.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.

feedbacks = feedback.objects.all()
students = student.objects.all()


def home(request):
    if request.user.is_authenticated:
        if manager.objects.filter(user=request.user).exists():
            return redirect('mess-about')
    return render(request,'mess/home.html',{'feedbacks':feedbacks,'students':students})

def about(request):
    return render(request,'mess/about.html')