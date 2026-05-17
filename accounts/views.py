import random

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout

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


#verify the user by using otp
def verify_otp(request,user_id):
    user=get_object_or_404(User,id=user_id)   #get rhe user

    if user.is_verified:                                        #if the person hit the refresh used to redirect to register page
        messages.warning(request,'user is already verified')
        return redirect('register')
    
    
    if request.method=='POST':
        entered_otp=request.POST.get('otp')
        otp=OTP.objects.filter(user=user,is_used=False).last()   #get the otp object

        if not otp:                                 #it execute if there is no otp object
            messages.warning(request,"no otp found")
            return redirect('register')
        
        if otp.is_expired():                        #if otp is not used more then 5 minits it expire
            messages.warning(request,'otp is expired')
            return redirect('register')
        
        if otp.attempts>=otp.max_attempts:          #if user try to verify wrong otp more then 5 times it show error and redirect to registe page
            messages.warning(request,'To many failed otp')
            return redirect('register')
               
        print(otp,entered_otp)
        if otp and otp.otp==entered_otp:           
            user.is_verified=True                                   #verify the user
            user.save()
            otp.is_used=True                                        #once user is verified then mark otp is used
            otp.save()
            messages.success(request,'user register succesfully')
            return redirect('register')
        else:
            
             
            otp.attempts+=1                                       #each failed attemp the otp attemp incersed
            otp.save()                                           #if user enter wrong otp it readierct to same page 
            if otp.attempts>=otp.max_attempts:                   #it back to the register form imidietly if the 5attemp close insted of rendering the verify otp page again
                messages.warning(request,'To many failed otp')
                return redirect('register')
            messages.warning(request,f"invalid otp {otp.max_attempts-otp.attempts} left")
            return redirect('verify_otp',user_id=user.id)       #i want to implemnet the counter to stop bryte force attack
    return render(request,'verify_otp.html')


def login_view(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        verified_user=User.objects.filter(email=email,is_verified=True).first()
        if not verified_user:
            messages.warning(request,"Invalid email or password.")
            return redirect('login')
        user=authenticate(request,username=email,password=password)
        if not user:
            messages.warning(request,"Invalid email or password.")
            return redirect('login')
        login(request,user)
        return redirect('home')

    return render(request,'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request,'home.html')