from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name='mess-home'),
    path('about/',views.about,name='mess-about'),
    path('reg_stu/',views.reg_stu,name='reg-stu'),
    path('reg_staff/',views.reg_staff,name='reg-staff'),
]