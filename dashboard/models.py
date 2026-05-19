from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.
class VendorRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
    ]

    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='vendor_requests')
    full_name=models.CharField(max_length=100)
    business_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=15)
    email=models.EmailField()
    status=models.CharField(max_length=30,choices=STATUS_CHOICES,default='pending')
    location=models.CharField(max_length=120)
    experience=models.TextField()

    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.full_name}-{self.status}'