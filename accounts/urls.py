from django.urls import include, path

from accounts import views

urlpatterns = [
    path('register/', views.register_view,name='register'),
    path('verify_otp/<int:user_id>/',views.verify_otp,name='verify_otp'),
]