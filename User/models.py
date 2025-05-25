from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserModel(AbstractUser):
    phone_number = models.CharField(max_length=12, default=None)
    password = models.CharField(max_length=128, default='defaultpassword')

    
    def __str__(self):
        return self.username