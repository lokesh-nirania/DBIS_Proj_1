from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class student(models.Model):
    name = models.CharField(max_length = 50)
    roll_number = models.IntegerField()
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        temp = str(self.roll_number)
        return temp

class manager(models.Model):
    name = models.CharField(max_length = 50)
    license_id = models.CharField(max_length = 50)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name