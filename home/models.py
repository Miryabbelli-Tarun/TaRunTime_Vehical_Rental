import uuid

from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model


User=get_user_model()


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=30,unique=True)
    slug=models.SlugField(blank=True,unique=True)
    image=models.ImageField(upload_to='category_images/')
    description=models.TextField()

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            short_id = str(uuid.uuid4())[:8]
            self.slug=slugify(f"{self.name}-{short_id}")
        return super(Category,self).save(*args,**kwargs)

    def __str__(self):
        return self.name

choices=[
    ('petrol','petrol'),
    ('electric','electric'),
    ('diesel','diesel')
]



class Vehicle(models.Model):
    vendor=models.ForeignKey(User,on_delete=models.CASCADE,related_name='vehicles')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='vehicles')
    name=models.CharField(max_length=40)
    vehicle_number=models.CharField(max_length=30,unique=True)
    slug=models.SlugField(blank=True,unique=True)
    model=models.CharField(max_length=40,null=True,blank=True)
    brand=models.CharField(max_length=40,null=True,blank=True)
    year=models.IntegerField()
    fuel_type=models.CharField(max_length=30,choices=choices)
    seat_capacity=models.IntegerField()
    mileage=models.IntegerField()
    price_per_day=models.DecimalField(max_digits=10,decimal_places=2)
    location=models.CharField(max_length=70)
    description=models.TextField(null=True,blank=True)
    image=models.ImageField(upload_to='vehicle_images/')
    availability=models.BooleanField(default=True)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            short_id = str(uuid.uuid4())[:8]
            self.slug=slugify(f"{self.name}-{short_id}")
        return super(Vehicle,self).save(*args,**kwargs)

    def __str__(self):
        return self.name


class Banner(models.Model):
    title=models.CharField(max_length=60)
    subtitle=models.CharField(max_length=60)
    image=models.ImageField(upload_to='banners/')
    button_link=models.CharField(max_length=100,blank=True,null=True)
    is_active=models.BooleanField(default=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title