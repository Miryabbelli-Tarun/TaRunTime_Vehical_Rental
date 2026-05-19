from django.urls import include, path

from home import views

urlpatterns = [    
    path('',views.home,name='home'),
    path('category-list/',views.category_list_view,name='category_list'),
    path('vehicle_details/<slug:vehicle_slug>/',views.vehicle_details_view,name='vehicle_details'),
    path('all_vehicles/',views.all_vehicles_view,name='all_vehicles'),
    path('about/',views.about_view,name='about'),
    path('contact/',views.contact_view,name='contact')

]