from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import student
from djmoney.models.fields import MoneyField
# Create your models here.

class feedback(models.Model):
    title = models.CharField(max_length = 50)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    roll_number = models.ForeignKey(student,on_delete=models.CASCADE)
    response = models.TextField()

    def __str__(self):
        return self.title

class staff(models.Model):
    name = models.CharField(max_length = 50)
    designation = models.CharField(max_length = 50)
    address = models.TextField()
    contact = models.CharField(max_length = 15)
    salary = MoneyField(max_digits=5, decimal_places=2, default_currency='INR')
    acc_no = models.CharField(max_length = 50)
    bank_name = models.CharField(max_length = 50)
    IFSC = models.CharField(max_length = 50)

    def __str__(self):
        return self.name