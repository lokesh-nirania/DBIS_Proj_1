from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from users.models import *
from django.contrib.auth.models import User

students = student.objects.all()
managers = manager.objects.all()
found = 0


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    found = 0
    for student in students:
        if student.user.username == request.user.username:
            found = 1
            type_is = "STUDENT"
            return render(request, 'users/profile.html',{'student':student,'type':type_is})
    for manager in managers:
        if manager.user.username == request.user.username:
            found = 1
            type_is = "MANAGER"
            return render(request, 'users/profile.html',{'manager':manager,'type':type_is})
    if found == 0:
        type_is = "NULL"
        return render(request, 'users/profile.html',{'found':found,'type':type_is})