from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    
    def __str__(self):
        return self.user