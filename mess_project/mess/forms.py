from django import forms
from djmoney.models.fields import MoneyField
from .models import *

class AddStaffForm(forms.ModelForm):
    class Meta:
        model = staff
        fields = (
            'staff_id',
            'name',
            'designation',
            'address',
            'contact',
            'salary',
            'acc_no',
            'bank_name',
            'IFSC',
        )

class UpdateStaffForm(forms.ModelForm):
    class Meta:
        model = staff
        fields = (
            'staff_id',
            'name',
            'designation',
            'address',
            'contact',
            'salary',
            'acc_no',
            'bank_name',
            'IFSC'
        )
        

class AddSupplierForm(forms.ModelForm):
    class Meta:
        model = supplier
        fields = (
            'sup_id',
            'name',
            'address',
            'contact',
        )

class AddPurchaseForm(forms.ModelForm):
    class Meta:
        model = purchase
        fields = (
            'pur_id',
            'sup_id',
            'bill_id',
            'item_id',
            'quantity',
            'amount'
        )

class AddConsumeForm(forms.ModelForm):
    class Meta:
        model = consumption
        fields = (
            'item_id',
            'quantity',
            'date'
        )

class AddBillForm(forms.ModelForm):
    class Meta:
        model = bill
        fields = (
            'bill_id',
            'date',
            'amount',
            'paid',
        )
class AddFeedbackForm(forms.ModelForm):
    class Meta:
        model = feedback
        fields = (
            'title',
            'content',
        )
class UpdateFeedbackForm(forms.Form):
    fb_id = forms.IntegerField()
    response = forms.CharField(max_length=125)