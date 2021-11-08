from django.contrib import admin
from .models import Product, BlackBox, BlackBoxItem


admin.site.register(Product)
admin.site.register(BlackBox)
admin.site.register(BlackBoxItem)
