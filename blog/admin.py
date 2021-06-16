from django.contrib import admin
from .models import Product, Category, Configure, Attribute

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Configure)
admin.site.register(Attribute)
