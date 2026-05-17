from django.shortcuts import render

from home.models import Banner, Category

# Create your views here.
def home(request):
    categories=Category.objects.all()
    banners=Banner.objects.filter(is_active=True)

    context={
        "categories":categories,
        'banners':banners
    }
    return render(request,'home.html',context)