from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name='mess-home'),
    path('see-menu',views.pdf_view,name='see-menu'),    
    path('about/',views.about,name='mess-about'),
    path('reg_stu/',views.reg_stu,name='reg-stu'),
    path('reg_staff/',views.reg_staff,name='reg-staff'),
    path('reg_supplier/',views.reg_supplier,name='reg-supplier'),
    path('bills/',views.bills,name='bills'),
    path('inventory/',views.inventor,name='inventory'),
    path('purchases/',views.purchas,name='purchase'),
    path('manage_feedback/',views.manager_feedback,name='manager_feedback'),
    path('consumes/',views.consum,name='consumes'),
    path('add_staff/',views.add_staff,name='add_staff'),
    path('add_supplier/',views.add_supplier,name='add_supplier'),
    path('add_bills/',views.add_bills,name='add_bill'),
    path('add_purchase/',views.add_purchase,name='add_purchase'),
    path('add_consumes/',views.add_consume,name='add_consume'),
    path('add_fb/',views.add_feedback,name='add_feedback'),
]
