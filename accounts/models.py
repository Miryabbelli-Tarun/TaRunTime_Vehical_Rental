from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts.manager import CustomUserManager
# Create your models here.
class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=100,unique=False)
    phone_number=models.CharField(max_length=11,blank=True,null=True)
    is_verified=models.BooleanField(default=False)
    is_vendor=models.BooleanField(default=False)
    wants_vendor=models.BooleanField(default=False)

    objects=CustomUserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.email
    
class OTP(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='otp')
    otp=models.CharField(max_length=6)
    is_used=models.BooleanField(default=False)

    attempts=models.IntegerField(default=0)
    max_attempts=models.IntegerField(default=5)

    

    def __str__(self):
        return f"{self.user.email}-{self.otp}"