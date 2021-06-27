from django.contrib import admin
from .models import Product, Category, Configure, Attribute, Cart, Order

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Configure)
admin.site.register(Attribute)
admin.site.register(Cart)
admin.site.register(Order)
# admin.site.register(CartManager)