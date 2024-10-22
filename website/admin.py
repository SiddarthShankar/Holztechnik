from django.contrib import admin
from .models import Customer, Order, OrderSpecs, Picking

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderSpecs)
admin.site.register(Picking)