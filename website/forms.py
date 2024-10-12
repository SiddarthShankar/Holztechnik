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
    order_id = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"placeholder": "Order Number", "class": "form-control"}), label="")
    status = forms.Select(choices=Order.STATUS),
    description = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "description", "class": "form-control"}), label="")
    class Meta:
        model = Order
        exclude = ("user",)
        

        