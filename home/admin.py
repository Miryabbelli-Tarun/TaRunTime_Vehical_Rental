from django.contrib import admin

from home.models import Banner, Category, Vehicle

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','created_at']
    search_fields=['name']

class VehicleAdmin(admin.ModelAdmin):
    list_display=['name','category','vendor','vehicle_number','seat_capacity','price_per_day']
    search_fields=['name','vehicle_number']

class BannerAdmin(admin.ModelAdmin):
    list_display=['title','subtitle','is_active']
    search_fields=['title','subtitle']
    list_filter=['is_active']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Vehicle,VehicleAdmin)
admin.site.register(Banner,BannerAdmin)