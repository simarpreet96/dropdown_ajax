from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.product_add, name='product_add'),
    path('index/', views.index, name='index'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),

]
