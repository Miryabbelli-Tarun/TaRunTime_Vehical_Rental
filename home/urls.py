from django.urls import include, path

from home import views

urlpatterns = [    
    path('',views.home,name='home'),
    path('category-list/',views.category_list_view,name='category_list'),
    path('vehicle_details/<slug:vehicle_slug>/',views.vehicle_details_view,name='vehicle_details'),

]