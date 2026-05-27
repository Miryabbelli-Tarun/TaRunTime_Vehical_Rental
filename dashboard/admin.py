from django.contrib import admin

from dashboard.models import Cart, VendorRequest

# Register your models here.
class VendorRequestAdmin(admin.ModelAdmin):
    list_display=['full_name','status','email','phone_number']
    list_filter=['status']
    search_fields=['full_name']
admin.site.register(VendorRequest,VendorRequestAdmin)
admin.site.register(Cart)