from django.shortcuts import render

from home.models import Banner, Category

# Create your views here.
def home(request):
    categories=Category.objects.all().order_by('?')[:6]
    banners=Banner.objects.filter(is_active=True)
    
    context={
        "categories":categories,
        'banners':banners
    }
    return render(request,'home.html',context)

def category_list_view(request):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(request,'category_list.html',context)