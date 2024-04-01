from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Reward(models.Model):
    reward_name = models.CharField(max_length=100)
    points_requirement = models.IntegerField()

class CustomUser(AbstractUser):
    birthday = models.DateField(blank=True, null=True)
    picture = models.CharField(max_length=1000, blank=True, null=True,)
    phone = models.CharField(max_length=20, blank=True, null=True)
    points_history = models.IntegerField(default=0)
    active_points = models.IntegerField(default=0)
    rewards = models.ManyToManyField(Reward)
    pass

class Receipt(models.Model):
    raw_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image_identifier = models.CharField(max_length=255, unique=True)


class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
