from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderSpecs)
admin.site.register(Picking)
admin.site.register(LedMapping)