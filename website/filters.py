import django_filters 
from .models import *

class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = {'customer_id', 'name'}
        
class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['status']