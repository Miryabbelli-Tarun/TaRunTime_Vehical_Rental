from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model

from dashboard.models import VendorRequest

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