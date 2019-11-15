from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name='mess-home'),
    path('about/',views.about,name='mess-about')
]