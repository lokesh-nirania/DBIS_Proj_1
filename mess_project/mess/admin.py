from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(feedback)
admin.site.register(staff)
# admin.site.register(item)
admin.site.register(inventory)
admin.site.register(supplier)
admin.site.register(bill)
admin.site.register(purchase)
admin.site.register(consumption)
admin.site.register(expenses)