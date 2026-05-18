from django.shortcuts import get_object_or_404, render
from django.db.models import Q
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


def all_vehicles_view(request):
    vehicles=Vehicle.objects.all()
    categories=Category.objects.all()

    if request.method=='GET':

        #nav bar serach button filtering by city,model,descriptin,name,model
        
        if request.GET.get('search'):
            search=request.GET.get('search')
            vehicles=vehicles.filter(Q(name__icontains=search) |  
                                     Q(model__icontains=search) | 
                                     Q(brand__icontains=search) | 
                                     Q(location__icontains=search) | 
                                     Q(description__icontains=search)
                                    )


        #sort by prices and latest filter section
        if request.GET.get('sort'):
            if request.GET.get('sort')=='low_to_high':
                vehicles=vehicles.order_by('price_per_day')
            elif request.GET.get('sort')=='high_to_low':
                vehicles=vehicles.order_by('-price_per_day')
            elif request.GET.get('sort')=='latest':
                vehicles=vehicles.order_by('-created_at')

        #price range filter
        if request.GET.get('min_price') or request.GET.get('max_price'):
            if request.GET.get('min_price'):
                vehicles=vehicles.filter(price_per_day__gte=request.GET.get('min_price'))
            if request.GET.get('max_price'):
                vehicles=vehicles.filter(price_per_day__lte=request.GET.get('max_price'))
        
        #category filter
        if request.GET.getlist('category'):
            print(request.GET.getlist('category'))
            vehicles=vehicles.filter(category__slug__in=request.GET.getlist('category'))

        #fuel type filter
        if request.GET.getlist('fuel_type'):
            # print(request.GET.getlist('fuel_type'))
            vehicles=vehicles.filter(fuel_type__in=request.GET.getlist('fuel_type'))

        #filter vehicles based on seat capacity
        if request.GET.get('capacity'):
            vehicles=vehicles.filter(seat_capacity__gte=request.GET.get('capacity'))
        
        #filter based on availability
        if request.GET.get('available'):
            vehicles=vehicles.filter(availability=True)
    context={
        'vehicles':vehicles,
        'categories':categories,
    }
    return render(request,'all_vehicles.html',context)