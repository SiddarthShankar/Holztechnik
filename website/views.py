from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Order
from .forms import *

@csrf_exempt

# Create your views here.
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    
    context = {'customers':customers, 'orders':orders}

    # Check if logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authentication step
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been successfully logged in!")     
            # Redirect based on user type
            if user.username == 'Vorgesetzter':
                return redirect('home')  # Redirect Vorgesetzter to home page
            elif user.username == 'Endfertigungteckniker':
                return redirect('order')  # Redirect Endfertigungteckniker to order page
            else:
                messages.error(request, "An error occurred, please try again!")
                return redirect('home')
        else:
            messages.error(request, "An error occurred, please try again!")
            return redirect('home')
    else:
        return render(request, 'home.html', context)
    
def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been successfully Logged Out!!...."))
    return redirect('home')

def about(request):
    if request.user.is_authenticated:
        return render(request, 'about.html', {'about':about})
    else:
        messages.success(request, ("You must be logged into access the data"))
        return redirect('home') 
    
def increase_font_size(request):
    current_size = request.session.get('font_size', 16)
    new_size = min(current_size + 2, 30)  # Increase by 2px, with a maximum size of 20px
    request.session['font_size'] = new_size
    return redirect(request.META.get('HTTP_REFERER', '/'))

def decrease_font_size(request):
    current_size = request.session.get('font_size', 16)
    new_size = max(current_size - 2, 12)  # Decrease by 2px, with a minimum size of 12px
    request.session['font_size'] = new_size
    return redirect(request.META.get('HTTP_REFERER', '/'))

def switch_theme(request, theme_name):
    request.session['theme'] = theme_name
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_num = Customer.objects.get(id=pk)
        context = {
            'customer_num':customer_num,
        }
        return render(request, 'customer.html', context)
    else:
        messages.success(request, ("You must be logged into access the data"))
        return redirect('home') 

def delete_CustomerDetails(request, pk):
    if request.user.is_authenticated:
        delete_detail = Customer.objects.get(id=pk)
        delete_detail.delete()
        messages.success(request, "Details have been deleted successfully!!..")
        return redirect('home') 
    else:
        messages.success(request, "You must be logged into access the data")
        return redirect('home') 

def add_CustomerDetails(request):
    customer_form = AddCustomerRecordForm(request.POST or None) 
    if request.user.is_authenticated:
        if request.method == "POST":
            if customer_form.is_valid():
                add_CustomerDetails = customer_form.save()
                messages.success(request, ("Details added successfully!!..."))
                return redirect('home')
        return render(request, 'add_CustomerDetails.html', {'customer_form':customer_form})
    else:
        messages.success(request, ("You must be logged in to add a form"))
        return redirect('home')
     
def update_CustomerDetails(request, pk):
    if request.user.is_authenticated:
        current_detail = Customer.objects.get(id=pk)
        customer_form = AddCustomerRecordForm(request.POST or None, instance=current_detail)
        if customer_form.is_valid():
            customer_form.save() 
            messages.success(request, ("Details have been Updated successfully!!.."))
            return redirect('home') 
        return render(request, 'update_CustomerDetails.html', {'customer_form':customer_form})
    else:
        messages.success(request, ("You must be logged into access the data"))
        return redirect('home') 

def order(request):
    if request.user.is_authenticated:
        return render(request, 'order.html', {'order':order})
    else:
        messages.success(request, ("You must be logged into access the data"))
        return redirect('home') 
    
def add_OrderDetails(request):
    order_form = AddOrderRecordForm(request.POST or None) 
    if request.user.is_authenticated:
        if request.method == "POST":
            if order_form.is_valid():
                add_OrderDetails = order_form.save()
                messages.success(request, ("Details added successfully!!..."))
                return redirect('/')
        return render(request, 'add_OrderDetails.html', {'order_form':order_form})
    else:
        messages.success(request, ("You must be logged in to add a form"))
        return redirect('home')
     