from django.contrib import admin
from django.contrib.auth import get_user_model

from accounts.models import OTP
User=get_user_model()
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=['username','email','is_verified','is_vendor']
    search_fields=['email','username']
    list_filter=['is_verified']

admin.site.register(User,UserAdmin)



class OtpAdmin(admin.ModelAdmin):
    list_display=['otp','user','is_used']
admin.site.register(OTP,OtpAdmin)