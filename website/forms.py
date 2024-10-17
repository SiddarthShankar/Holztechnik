from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from django.utils.translation import gettext as _
from .models import *

class AddCustomerRecordForm(forms.ModelForm):
    customer_id = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"placeholder": _("Customer Number"), "class": "form-control"}), label="")
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": _("Name"), "class": "form-control"}), label="")
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": _("Email"), "class": "form-control"}), label="")
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": _("Phone"), "class": "form-control"}), label="")
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": _("Address"), "class": "form-control"}), label="")
   
    class Meta:
        model = Customer
        exclude = ("user",)

class AddOrderRecordForm(forms.ModelForm):
    order_id = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": _("Order Number"), "class": "form-control"}), label="")
    status = forms.ChoiceField(choices=Order.STATUS, widget=forms.Select(attrs={"placeholder": _("Status"), "class": "form-control"}), label="")
    description = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": _("Description"), "class": "form-control"}), label="")
    
    class Meta:
        model = Order
        fields = ['order_id', 'status', 'description', 'customer',]
    
    def __init__(self, *args, **kwargs):
        # Extract the customer from the passed arguments if it's present
        customer = kwargs.pop('customer', None)
        super(AddOrderRecordForm, self).__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs.update({"class": "form-control"})

class AddOrderSpecsForm(forms.ModelForm):
    order = forms.ModelChoiceField(queryset=Order.objects.all(), required=True, widget=forms.Select(attrs={"class": "form-control"}), label="")
    article = forms.CharField(widget=forms.TextInput(attrs={"placeholder": _("Article"), "class": "form-control"}), label="")
    pieces = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": _("Pieces"), "class": "form-control"}), label="" )
    material = forms.CharField(widget=forms.TextInput(attrs={"placeholder": _("Material"), "class": "form-control"}), label="")
    length = forms.DecimalField(widget=forms.NumberInput(attrs={"placeholder": _("Length (in meters)"), "class": "form-control"}), label="" )
    breadth = forms.DecimalField(widget=forms.NumberInput(attrs={"placeholder": _("Breadth (in meters)"), "class": "form-control"}), label="" )
    thickness = forms.DecimalField(widget=forms.NumberInput(attrs={"placeholder": _("Thickness (in meters)"), "class": "form-control"}), label="")
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": _("Quantity"), "class": "form-control"}),label="")
    pricePerMeter = forms.DecimalField( widget=forms.NumberInput(attrs={"placeholder": _("Price Per Meter"), "class": "form-control"}), label="")

    class Meta:
        model = OrderSpecs
        fields = ['order', 'article', 'pieces', 'material', 'length', 'breadth', 'thickness', 'quantity', 'pricePerMeter']

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }