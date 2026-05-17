from django.urls import include, path

from home import views

urlpatterns = [    
    path('',views.home,name='home'),
    path('category-list/',views.category_list_view,name='category_list'),

]