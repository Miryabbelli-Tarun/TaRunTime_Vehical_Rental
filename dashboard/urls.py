from django.urls import  path

from dashboard import views

urlpatterns = [    
    path('profile/',views.profile_view,name='profile'),
    path('apply-for-vendor/',views.apply_vendor_view,name='apply_vendor'),
    path('approve_vendor_requests/',views.approve_vendor_requests_view,name='approve_vendor_requests'),
    path('approve_vendor/<int:id>/',views.approve_vendor_view,name='approve_vendor'),
    path('reject_vendor/<int:id>/',views.reject_vendor_view,name='reject_vendor'),
    path('add_vehicle/',views.add_vehicle_view,name='add_vehicle'),
    path('my_vehicles/',views.my_vehicles_view,name='my_vehicles'),
    path('edit_vendor_vehicle/<slug:slug>/',views.edit_vendor_vehicle_view,name="edit_vendor_vehicle"),
    path('delete_vendor_vehicle/<slug:slug>/',views.delete_vendor_vehicle_view,name='delete_vendor_vehicle'),
]