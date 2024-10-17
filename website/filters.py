import django_filters 
from django.utils.translation import gettext as _
from .models import *

class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = {_('customer_id'), _('name')}
        
class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = [_('status')]