from django.urls import  path

from dashboard import views

urlpatterns = [    
    path('profile/',views.profile_view,name='profile'),
    path('apply-for-vendor/',views.apply_vendor_view,name='apply_vendor'),
    path('approve_vendor_requests/',views.approve_vendor_requests_view,name='approve_vendor_requests'),
    path('approve_vendor/<int:id>/',views.approve_vendor_view,name='approve_vendor'),
    path('reject_vendor/<int:id>/',views.reject_vendor_view,name='reject_vendor'),
]