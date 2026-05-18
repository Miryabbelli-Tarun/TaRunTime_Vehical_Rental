from django.shortcuts import get_object_or_404, render

from home.models import Banner, Category, Vehicle

# Create your views here.
def home(request):
    categories=Category.objects.all().order_by('?')[:6]
    banners=Banner.objects.filter(is_active=True)
    vehicles=Vehicle.objects.filter(availability=True)
    
    context={
        "categories":categories,
        'banners':banners,
        'vehicles':vehicles
    }
    return render(request,'home.html',context)

def category_list_view(request):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(request,'category_list.html',context)


def vehicle_details_view(request,vehicle_slug):
    vehicle=get_object_or_404(Vehicle,slug=vehicle_slug)
    # print(vehicle)
    context={
        'vehicle':vehicle,
    }
    return render(request,'vehicle_details.html',context)