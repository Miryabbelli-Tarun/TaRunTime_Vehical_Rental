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

    #cart functionality
    path('cart/',views.cart_view,name='cart'),
    path('add_to_cart/<slug:slug>/',views.add_to_cart_view,name="add_to_cart"),
    path('remove_cart_item/<int:id>/',views.remove_cart_item_view,name='remove_cart_item'),

    #wishlist
    path('wishlist/',views.wishlist_view,name='wishlist'),
    path('toggle_wishlist/<slug:slug>/',views.toggle_wishlist_view,name='toggle_wishlist'),
    path('remove_from_wishlist/<int:id>/',views.remove_from_wishlist_view,name='remove_from_wishlist'),


    #booking requests
    path('booking_vehicle/<int:id>/',views.checkout_view,name='checkout'),
    path('my_bookings/',views.my_bookings_view,name='my_bookings'),
    path('vendor_booking_requests/',views.vendor_booking_requests_view,name="vendor_booking_requests"),
    path('approve_booking_request/<int:id>/',views.approve_booking_request_view,name="approve_booking_request"),
    path('reject_booking_request/<int:id>/',views.reject_booking_request_view,name="reject_booking_request"),
]