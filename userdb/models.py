from django.db import models


# Create your models here.
class User_Data(models.Model):
    user_id=models.AutoField(primary_key=True)
    state = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    district = models.CharField(max_length=40,default='bangalore urban')
    available_capacity = models.CharField(max_length=10,default='_dose1')
    toaddr = models.CharField(max_length=50)
    quantity=models.IntegerField(default=1)
