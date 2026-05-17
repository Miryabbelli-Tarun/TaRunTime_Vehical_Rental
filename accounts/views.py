import random

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model

from accounts.models import OTP


User=get_user_model()

# Create your views here.
def register_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')

        if password!=confirm_password:
            messages.warning(request,'password not match')
            return redirect('register')
        
        verified_user=User.objects.filter(email=email,is_verified=True).first()
        if  verified_user:
            messages.warning(request,'user with email already exists')
            return redirect('register')
        user=User.objects.filter(email=email,is_verified=False).first()    #if a user register but not verify is account then it return their account insted of again creating
        if not user:                                               #this create new user
            user=User.objects.create(email=email,
                                     username=username,
                                     phone_number=phone_number)
        else:                                                      #if user come back without verify account in otp page then user enter new details insted of old details then it store the new details insted of old details
            user.username=username
            user.phone_number=phone_number
        user.set_password(password)
        user.save()
        OTP.objects.filter(user=user,is_used=False).delete()    #delete previous unused otp to generate new otp
        otp=str(
            random.randint(100000,999999)
        )
        print(otp)
        OTP.objects.create(user=user,otp=otp,is_used=False)
        return redirect('verify_otp',user_id=user.id)
        

    return render(request,'register.html')

def verify_otp(request,user_id):
    user=get_object_or_404(User,id=user_id)   #get rhe user

    if user.is_verified:                                        #if the person hit the refresh used to redirect to register page
        messages.warning(request,'user is already verified')
        return redirect('register')
    
    if request.method=='POST':
        entered_otp=request.POST.get('otp')
        otp=OTP.objects.filter(user=user,otp=entered_otp,is_used=False).last()   #get the otp object
        
        print(otp,entered_otp)
        if otp:
            
            user.is_verified=True          #verify the user
            user.save()
            otp.is_used=True            #once user is verified then mark otp is used
            otp.save()
            messages.success(request,'user register succesfully')
            return redirect('register')
        else:
            messages.warning(request,'invalid otp')             #if user enter wrong otp it readierct to same page 
            return redirect('verify_otp',user_id=user.id)       #i want to implemnet the counter to stop bryte force attack
    return render(request,'verify_otp.html')