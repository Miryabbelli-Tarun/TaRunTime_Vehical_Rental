from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model

from dashboard.models import Cart, VendorRequest, Wishlist
from home.models import Category, Vehicle
from datetime import datetime

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


def delete_vendor_vehicle_view(request,slug):
    vehicle=get_object_or_404(Vehicle,slug=slug)
    if request.user!=vehicle.vendor:
        messages.warning(request,"access denied")
        return redirect('profile')
    if request.method=="POST":
        vehicle.delete()  
        messages.success(request,"vehicle delete succesfully")
        return redirect('my_vehicles')
    return redirect('my_vehicles')




#add to cart view
def add_to_cart_view(request,slug):
    user=request.user
    vehicle=get_object_or_404(Vehicle,slug=slug)
    if not user:
        messages.warning(request,"access denied")
        return redirect('profile')
    if request.method=='POST':
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        print(start_date,end_date,sep="             ")
        #calculate dates and amount
        start=datetime.strptime(start_date,"%Y-%m-%d").date()
        end=datetime.strptime(end_date,"%Y-%m-%d").date()
        print(start,end,sep="          ")
        total_days=(end-start).days
        if total_days<=0:
            messages.warning(request,"invalid dates")
            return redirect('vehicle_details',slug=vehicle.slug)
        amount=(total_days*vehicle.price_per_day)


        # check duplicate cart item

        existing_cart_item = Cart.objects.filter(

            user=request.user,

            vehicle=vehicle,

            start_date=start_date,

            end_date=end_date

        ).exists()


        if existing_cart_item:

            messages.warning(
                request,
                'Vehicle already added to cart'
            )

            return redirect('cart')


        Cart.objects.create(
            user=user,
            vehicle=vehicle,
            start_date=start_date,
            end_date=end_date,
            total_days=total_days,
            amount=amount
        )
        messages.success(request,"vehicle added to cart succesfully")
        return redirect('cart')

    

    return redirect('vehicle_details',slug=vehicle.slug)
    


def cart_view(request):
    cart_items=Cart.objects.filter(user=request.user).select_related('vehicle')
    total_amount=sum(item.amount for item in cart_items)
    context={
        'cart_items':cart_items,
        "total_amount":total_amount
    }
    return render(request,"dashboard/cart.html",context)

def remove_cart_item_view(request,id):
    item=get_object_or_404(Cart,id=id,user=request.user)
    item.delete()
    messages.success(request,'vehicle removed from cart')
    return redirect('cart')

#========================
#wish list functionalitys
#========================



def wishlist_view(request):
    wishlist_items=Wishlist.objects.filter(user=request.user).select_related('vehicle')
    context={
        "wishlist_items":wishlist_items
    }
    return render(request,'dashboard/wishlist.html',context)

def toggle_wishlist_view(request,slug):
    vehicle=get_object_or_404(Vehicle,slug=slug)
    wishlist_item=Wishlist.objects.filter(user=request.user,vehicle=vehicle).first()
    if wishlist_item:
        wishlist_item.delete()
        messages.warning(request," removed from wishlist")
        
    else:
        Wishlist.objects.create(
            user=request.user,
            vehicle=vehicle
        )
        messages.success(request,"vehicle added to wishlist")
    return redirect('vehicle_details',vehicle_slug=vehicle.slug)

def remove_from_wishlist_view(request,id):
    item=get_object_or_404(Wishlist,id=id,user=request.user)
    item.delete()
    messages.success(request,"vehicle removed from wishlist")
    return redirect('wishlist')
    