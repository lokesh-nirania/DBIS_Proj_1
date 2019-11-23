from django.shortcuts import render, redirect
from mess.models import *
from users.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from .forms import *
from django.http import FileResponse, Http404


# Create your views here.

feedbacks = feedback.objects.all().order_by('-date_created')
students = student.objects.all()
inven = inventory.objects.all()
unpaid = 0
unresponded = 0
expenditure = 0
for entry in bill.objects.all():
    if entry.paid == False:
        unpaid = unpaid + 1
    else:
        expenditure = expenditure + entry.amount
for entry in feedbacks:
    if entry.response == "":
        unresponded = unresponded + 1

data = {
    'feedbacks' : feedbacks,
    'students' : students,
    'staffs' : staff.objects.all(),
    'inventory' : inventory.objects.all(),
    'suppliers' : supplier.objects.all(),
    'bills' : bill.objects.all().order_by('-date'),
    'purchases' : purchase.objects.all(),
    'consumptions' : consumption.objects.all(),
    'expenses' : expenditure,
    'unpaid_bills_count' : unpaid,
    'unresponded_feedbacks' : unresponded,
}
@login_required
def add_staff(request):
    if request.method == 'POST':
        form = AddStaffForm(request.POST)
        form.save()
        iid = form.cleaned_data.get('staff_id')
        sname = form.cleaned_data.get('name')
        messages.success(request, f'{sname} added with staff_id {iid}!')
        # data.update({
        #     'staffs' : staff.objects.all(),
        #     }),
        return redirect('reg-staff')
    else:
        if request.user.is_authenticated:
            if manager.objects.filter(user=request.user).exists():
                form = AddStaffForm()
                return render(request,'mess/add_staff.html',{'form':form})
            else:
                return HttpResponseForbidden()

@login_required
def add_feedback(request):
    if request.method == 'POST':
        form = AddFeedbackForm(request.POST)
        post = form.save(commit=False)
        post.user = request.user
        post.date_created = timezone.now()
        post.save()
        # iid = post.cleaned_data.get('title')
        messages.success(request, f'Feedback added ')
        return redirect('mess-home')
    else:
        if request.user.is_authenticated:
            form = AddFeedbackForm()
            return render(request,'mess/add_feedback.html',{'form':form})
            

@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = AddSupplierForm(request.POST)
        if form.is_valid:
            form.save()
            iid = form.cleaned_data.get('name')
            messages.success(request, f'Supplier added with Name {iid}!')
            return redirect('reg-supplier')
        else:
            messages.success(request, f'Supplier ID already Exists!')
            return redirect('add_supplier')
    else:
        if request.user.is_authenticated:
            if manager.objects.filter(user=request.user).exists():
                form = AddSupplierForm()
                return render(request,'mess/add_supplier.html',{'form':form})
            else:
                return HttpResponseForbidden()

@login_required
def manager_feedback(request):
    if request.method == 'POST':
        form = UpdateFeedbackForm(request.POST)
        obj = feedback.objects.get(id=request.POST.get('fb_id'))
        obj.response = request.POST.get('response')
        obj.save()
        print("-------------------------------------------------------")
        print(obj.response)
        data.update({
            'feedbacks' : feedback.objects.all().order_by('-date_created'),
            'students' : student.objects.all(),
        })
        return render(request,'mess/manager_feedback.html',data)
    else:
        if request.user.is_authenticated:
            if manager.objects.filter(user=request.user).exists():
                return render(request,'mess/manager_feedback.html',data)
            else:
                return HttpResponseForbidden()

def add_bills(request):
    if request.method == 'POST':
        form = AddBillForm(request.POST)
        form.save()
        iid = form.cleaned_data.get('amount')
        messages.success(request, f'Added bill of {iid}!')
        return redirect('bills')
    else:
        if request.user.is_authenticated:
            if manager.objects.filter(user=request.user).exists():
                form = AddBillForm()
                return render(request,'mess/add_bills.html',{'form':form})
            else:
                return HttpResponseForbidden()

@login_required
def add_purchase(request):
    if request.method == 'POST':
        form = AddPurchaseForm(request.POST)
        if form.is_valid():
            iid = form.cleaned_data.get('item_id')
            iid = str(iid)
            bil_id = form.cleaned_data.get('bill_id')
            print(bil_id)
            qty = form.cleaned_data.get('quantity')
            qty = str(qty)
            print(qty)
            form.save()
            obj = inven.get(name=iid)
            obj_qty = obj.quantity
            obj.quantity = str(int(qty) + int(obj_qty))
            obj.save()
            print('invetory updated')
            iid = form.cleaned_data.get('amount')
            messages.success(request, f'Purchase added with Amount {iid}!')
            
            bills = bill.objects.get(bill_id=bil_id)
            print(bills)
            return redirect('purchase')
        else:
            messages.success(request, f'Purchase ID already Exists!')
            return redirect('add_purchase')
    else:
        if request.user.is_authenticated:
            if manager.objects.filter(user=request.user).exists():
                form = AddPurchaseForm()
                temp = {
                    'form' : form,
                }
                data.update(temp)
                return render(request,'mess/add_purchase.html',data)
            else:
                return HttpResponseForbidden()

@login_required
def add_consume(request):
    if request.method == 'POST':
        form = AddConsumeForm(request.POST)
        if form.is_valid():
            iid = form.cleaned_data.get('item_id')
            iid = str(iid)
            print(iid)
            qty = form.cleaned_data.get('quantity')
            qty = str(qty)
            print(qty)
            form.save()
            obj = inven.get(name=iid)
            obj_qty = obj.quantity
            obj.quantity = str(int(obj_qty) - int(qty))
            if int(obj.quantity) < 0:
                messages.success(request, f'Consume Exceeded on available')
                return redirect('add_consume')
            else:
                obj.save()
                messages.success(request, f'{iid}! is consumed by quantity {qty}')
                return redirect('consumes')
        else:
            messages.success(request, f'Invaild Form')
            return redirect('add_consume')
    else:
        if request.user.is_authenticated:
            if manager.objects.filter(user=request.user).exists():
                form = AddConsumeForm()
                temp = {
                    'form' : form,
                }
                data.update(temp)
                return render(request,'mess/add_consumes.html',data)
            else:
                return HttpResponseForbidden()

def home(request):
    if request.method == 'POST':
        fid = request.POST.get('id')
        ft = feedback.objects.get(id=int(fid)).title
        feedback.objects.filter(id=int(fid)).delete()
        messages.success(request, f'Feedback "{ ft }" is deleted successfully')
        return redirect('mess-home')
    else :
        if request.user.is_authenticated:
            if manager.objects.filter(user=request.user).exists():
                return render(request,'mess/manager_home.html',data)
        data.update({
            'feedbacks' : feedback.objects.all().order_by('-date_created'),
            'students' : student.objects.all(),
            'flag' : request.user.is_authenticated,
            'id' : request.user
        })
        return render(request,'mess/home.html',data)

def about(request):
    return render(request,'mess/about.html')

@login_required
def reg_stu(request):
    if request.user.is_authenticated:
        if manager.objects.filter(user=request.user).exists():
            data.update({
            'students' : student.objects.all(),
            }),
            return render(request,'mess/registered_student_list.html',data)
        else:
            return HttpResponseForbidden()

@login_required
def reg_staff(request):
    if request.method == 'POST':
        iid = request.POST.get('staff_id')
        sname = staff.objects.get(staff_id=iid)
        staff.objects.filter(staff_id=request.POST.get('staff_id')).delete()
        data.update({
            'staffs' : staff.objects.all(),
            }),
        messages.success(request, f'{sname} deleted with Staff ID { iid } ')
        return render(request,'mess/registered_staff_list.html',data)
    else :
        data.update({
            'staffs' : staff.objects.all(),
            }),
        if request.user.is_authenticated:
            if manager.objects.filter(user=request.user).exists():
                return render(request,'mess/registered_staff_list.html',data)
            else:
                return HttpResponseForbidden()

@login_required
def reg_supplier(request):
    if request.method == 'POST':
        iid = request.POST.get('sup_id')
        sname = supplier.objects.get(sup_id=iid)
        supplier.objects.filter(sup_id=request.POST.get('sup_id')).delete()
        data.update({
            'suppliers' : supplier.objects.all(),
            }),
        messages.success(request, f'{sname} deleted with Supplier ID { iid } ')
        return render(request,'mess/registered_supplier_list.html',data)
    else :
        if request.user.is_authenticated:
            if manager.objects.filter(user=request.user).exists():
                return render(request,'mess/registered_supplier_list.html',data)
            else:
                return HttpResponseForbidden()

@login_required
def purchas(request):
    if request.user.is_authenticated:
        if manager.objects.filter(user=request.user).exists():
            data.update({
                'purchases' : purchase.objects.all(),
            })
            return render(request,'mess/purchases.html',data)
        else:
            return HttpResponseForbidden()

@login_required
def consum(request):
    if request.user.is_authenticated:
        if manager.objects.filter(user=request.user).exists():
            data.update({
                'consume' : consumption.objects.all()
            })
            return render(request,'mess/consumes.html',data)
        else:
            return HttpResponseForbidden()

@login_required
def bills(request):
    if request.method == 'POST':
        print(request.POST.get('bill_id'))
        obj = bill.objects.get(bill_id=request.POST.get('bill_id'))
        status = obj.paid
        if status == True:
            obj.paid = False
            # obj.date_paid = None
        else:
            obj.paid = True
            # obj.paid_date = timezone.now()
        obj.save()
        unpaid = 0
        expenditure = 0
        for entry in bill.objects.all():
            if entry.paid == False:
                unpaid = unpaid + 1
            else:
                expenditure = expenditure + entry.amount
        data.update({
            'bills' : bill.objects.all().order_by('-date'),
            'expenses' : expenditure,
            'unpaid_bills_count' : unpaid,
            }),
        return render(request,'mess/bills.html',data)
    else :
        unpaid = 0
        expenditure = 0
        for entry in bill.objects.all():
            if entry.paid == False:
                unpaid = unpaid + 1
            else:
                expenditure = expenditure + entry.amount
        data.update({
            'bills' : bill.objects.all().order_by('-date'),
            'expenses' : expenditure,
            'unpaid_bills_count' : unpaid,
            }),
        if request.user.is_authenticated:
            if manager.objects.filter(user=request.user).exists():
                return render(request,'mess/bills.html',data)
            else:
                return HttpResponseForbidden()

@login_required
def inventor(request):
    if request.user.is_authenticated:
        if manager.objects.filter(user=request.user).exists():
            data.update({
                'inventory' : inventory.objects.all(),
            })
            return render(request,'mess/inventory.html',data)
        else:
            return HttpResponseForbidden()

def pdf_view(request):
    try:
        return FileResponse(open('mess/static/blog/mozilla.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
# def pdf_view(request):
#     with open('mess/static/blog/mozilla.pdf', 'r') as pdf:
#         response = HttpResponse(pdf.read(), contenttype='application/pdf')
#         response['Content-Disposition'] = 'inline;filename=some_file.pdf'
#         return response
#     pdf.closed