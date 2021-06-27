from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('product_add/', views.product_add, name='product_add'),
    path('cart_home/', views.cart_home, name='cart_home'),
    path('cart_update/', views.cart_update, name='cart_update'),
    path('product_detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),

]
