from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model

from dashboard.models import VendorRequest
from home.models import Category, Vehicle

User=get_user_model()
# Create your views here.
def profile_view(request):
    return render(request,'dashboard/profile.html')


#apply for vendor requests
def apply_vendor_view(request):
    if request.user.is_vendor:
        messages.warning(request,'you are already vendor')
        return redirect('profile')
    if request.method== 'POST':
        user=request.user
        full_name=request.POST.get('full_name')
        email=request.POST.get('email')
        business_name=request.POST.get('business_name')
        phone_number=request.POST.get('phone')
        location=request.POST.get('location')
        experience=request.POST.get('experience')

        if VendorRequest.objects.filter(user=request.user,status='pending').exists():
            messages.warning(request,'you are already applied for vendor')
            return redirect('apply_vendor')
        
        rejected_request = VendorRequest.objects.filter(
            user=request.user,
            status='rejected'
        ).first()


        # if rejected request exists -> update it

        if rejected_request:

            rejected_request.full_name = full_name

            rejected_request.email = email

            rejected_request.business_name = business_name

            rejected_request.phone_number = phone_number

            rejected_request.location = location

            rejected_request.experience = experience

            rejected_request.status = 'pending'

            rejected_request.save()

        else:
        
            VendorRequest.objects.create(
                user=user,
                full_name=full_name,
                business_name=business_name,
                phone_number=phone_number,
                email=email,
                location=location,
                experience=experience
                )
        request.user.wants_vendor=True
        request.user.save()
        messages.success(request,'Succesfully applied for the vendor')
        return redirect('apply_vendor')


    return render(request,'dashboard/vendor/apply_vendor.html')



#display the all requests on admin requests
def approve_vendor_requests_view(request):
    if not request.user.is_superuser:
        messages.warning(request,'access denied')
        return redirect('profile')
    vendor_requests=VendorRequest.objects.filter(status='pending')
    context={
        'vendor_requests':vendor_requests
    }
    return render(request,'dashboard/admin/approve_vendor_requests.html',context)



#approve vendor
def approve_vendor_view(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'access denied')
        return redirect('profile')
    vendor_request=get_object_or_404(VendorRequest,id=id)
    vendor_request.user.is_vendor=True
    vendor_request.user.wants_vendor=False
    vendor_request.user.save()
    vendor_request.status='approved'
    vendor_request.save()  
    messages.success(request,'vendor request accepted')
    return redirect('approve_vendor_requests')


#reject vendor
def reject_vendor_view(request,id):
    if not request.user.is_superuser:
        messages.warning(request,'access denied')
        return redirect('profile')
    
    vendor_request=get_object_or_404(VendorRequest,id=id)
    vendor_request.user.wants_vendor=False
    vendor_request.user.save()
    vendor_request.status='rejected'
    vendor_request.save()
    return redirect('approve_vendor_requests')




def add_vehicle_view(request):
    
    #check that users is vendor or not
    if not request.user.is_vendor:
        messages.warning(request,"access denied")
        return redirect('profile')
    categories=Category.objects.all()
    if request.method=='POST':
        vendor=request.user
        category=get_object_or_404(Category,id=request.POST.get('category'))
        name=request.POST.get('name')
        vehicle_number=request.POST.get('vehicle_number')
        model=request.POST.get('model')
        brand=request.POST.get('brand')
        year=request.POST.get('year')
        fuel_type=request.POST.get('fuel_type')
        seat_capacity=request.POST.get('seat_capacity')
        mileage=request.POST.get('mileage')
        price_per_day=request.POST.get('price_per_day')
        location=request.POST.get('location')
        description=request.POST.get('description')
        image=request.FILES.get('image')
        # print(vendor,category, name,vehicle_number,model ,brand,year,fuel_type,seat_capacity,mileage,price_per_day,location,description,image)
        vehicle=Vehicle.objects.create(
            vendor=request.user,
            category=category,
            name=name,
            vehicle_number=vehicle_number,
            model=model,
            brand=brand,
            year=year,
            fuel_type=fuel_type,
            seat_capacity=seat_capacity,
            mileage=mileage,
            price_per_day=price_per_day,
            location=location,
            description=description,
            image=image
        )
        messages.success(request,"vehicle added succesfully")
        return redirect('add_vehicle')

    context={
        'categories':categories
    }
    return render(request,'dashboard/vendor/add_vehicle.html',context)


def my_vehicles_view(request):
    vendor=request.user
    my_vehicles=vendor.vehicles.all()
    context={
        "my_vehicles":my_vehicles
    }
    return render(request,'dashboard/vendor/my_vehicles.html',context)

def edit_vendor_vehicle_view(request,slug):
    vehicle=get_object_or_404(Vehicle,slug=slug)
    if request.user!=vehicle.vendor:
        messages.warning(request,"Access denied")
        return redirect('profile')
    categories=Category.objects.all()
    
    if request.method=="POST":
        vehicle.name=request.POST.get('name')
        vehicle.category=get_object_or_404(Category,id=request.POST.get('category'))
        vehicle.vehicle_number=request.POST.get('vehicle_number')
        vehicle.model=request.POST.get('model')
        vehicle.brand=request.POST.get('brand')
        vehicle.year=request.POST.get('year')
        vehicle.fuel_type=request.POST.get('fuel_type')
        vehicle.seat_capacity=request.POST.get('seat_capacity')
        vehicle.mileage=request.POST.get('mileage')
        vehicle.price_per_day=request.POST.get('price_per_day')
        vehicle.location=request.POST.get('location')
        vehicle.description=request.POST.get('description')     
        vehicle.availability=(request.POST.get('availability')=="True")
        if request.FILES.get('image'):
            vehicle.image=request.FILES.get('image')
        vehicle.save()
        messages.success(request,"vehicle updated succesfully")
        return redirect('my_vehicles')

    context={
        'vehicle':vehicle,
        "categories":categories,
    }

    return render(request,'dashboard/vendor/edit_vendor_vehicle.html',context)