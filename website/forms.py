from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from .models import *

class AddCustomerRecordForm(forms.ModelForm):
    customer_id = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"placeholder": "Customer Number", "class": "form-control"}), label="")
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Name", "class": "form-control"}), label="")
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}), label="")
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Phone", "class": "form-control"}), label="")
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Address", "class": "form-control"}), label="")
   
    class Meta:
        model = Customer
        exclude = ("user",)

class AddOrderRecordForm(forms.ModelForm):
    order_id = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Order Number", "class": "form-control"}), label="")
    status = forms.ChoiceField(choices=Order.STATUS, widget=forms.Select(attrs={"placeholder": "Status", "class": "form-control"}), label="")
    description = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Description", "class": "form-control"}), label="")
    
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
    article = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Article", "class": "form-control"}), label="")
    pieces = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Pieces", "class": "form-control"}), label="" )
    material = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Material", "class": "form-control"}), label="")
    length = forms.DecimalField(widget=forms.NumberInput(attrs={"placeholder": "Length (in meters)", "class": "form-control"}), label="" )
    breadth = forms.DecimalField(widget=forms.NumberInput(attrs={"placeholder": "Breadth (in meters)", "class": "form-control"}), label="" )
    thickness = forms.DecimalField(widget=forms.NumberInput(attrs={"placeholder": "Thickness (in meters)", "class": "form-control"}), label="")
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Quantity", "class": "form-control"}),label="")
    pricePerMeter = forms.DecimalField( widget=forms.NumberInput(attrs={"placeholder": "Price Per Meter", "class": "form-control"}), label="")

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