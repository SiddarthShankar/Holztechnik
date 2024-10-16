from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Order, OrderSpecs
from .filters import OrderFilter, CustomerFilter
from django.utils.translation import gettext as _
from .forms import *

@csrf_exempt

# Create your views here.
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    myFilters = CustomerFilter(request.GET, queryset=customers)
    customers = myFilters.qs
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'customers':customers, 'orders':orders, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending, 'myFilters': myFilters}
    
    if request.method == 'GET' and 'order_id' in request.GET:
        order_id = request.GET.get('order_id')
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                return redirect('order', pk=order.id)
            except Order.DoesNotExist:
                messages.error(request, _("Order not found!"))
                
    # Check if logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authentication step
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, _("You have been successfully logged in!"))     
            # Redirect based on user type
            if user.username == 'Vorgesetzter':
                return redirect('home')  # Redirect Vorgesetzter to home page
            elif user.username == 'Endfertigungteckniker':
                return redirect('order')  # Redirect Endfertigungteckniker to order page
            else:
                messages.error(request, _("An error occurred, please try again!"))
                return redirect('home')
        else:
            messages.error(request, _("An error occurred, please try again!"))
            return redirect('home')
    else:
        return render(request, 'home.html', context)
    
def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, _("You have been successfully Logged Out!!...."))
    return redirect('home')

def about(request):
    if request.user.is_authenticated:
        return render(request, 'about.html', {'about':about})
    else:
        messages.success(request, _("You must be logged into access the data"))
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
        customer = get_object_or_404(Customer, id=pk)
        orders = customer.orders.all()  # Assuming 'orders' is a related name for customer orders
        context = {
            'customer_num': customer,
            'orders': orders
        }
        return render(request, 'customer.html', context)
    else:
        messages.success(request, _("You must be logged in to access the data"))
        return redirect('home')

def delete_CustomerDetails(request, pk):
    if request.user.is_authenticated:
        delete_detail = Customer.objects.get(id=pk)
        delete_detail.delete()
        messages.success(request, _("Details have been deleted successfully!!.."))
        return redirect('home') 
    else:
        messages.success(request, _("You must be logged into access the data"))
        return redirect('home') 

def add_CustomerDetails(request):
    customer_form = AddCustomerRecordForm(request.POST or None) 
    if request.user.is_authenticated:
        if request.method == "POST":
            if customer_form.is_valid():
                add_CustomerDetails = customer_form.save()
                messages.success(request, _("Details added successfully!!..."))
                return redirect('home')
        return render(request, 'add_CustomerDetails.html', {'customer_form':customer_form})
    else:
        messages.success(request, _("You must be logged in to add a form"))
        return redirect('home')
     
def update_CustomerDetails(request, pk):
    if request.user.is_authenticated:
        current_detail = Customer.objects.get(id=pk)
        customer_form = AddCustomerRecordForm(request.POST or None, instance=current_detail)
        if customer_form.is_valid():
            customer_form.save() 
            messages.success(request, _("Details have been Updated successfully!!.."))
            return redirect('home') 
        return render(request, 'update_CustomerDetails.html', {'customer_form':customer_form})
    else:
        messages.success(request, _("You must be logged into access the data"))
        return redirect('home') 

def order(request, pk):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, id=pk)
        orders = Order.objects.filter(customer=customer)
        orderspecs = OrderSpecs.objects.filter(order__customer=customer)
        
        context = {
            'customer_num': customer,
            'orders': orders,
            'orderspecs': orderspecs,
        }
        return render(request, 'order.html', context)
    else:
        messages.error(request, _("You must be logged in to access the data"))
        return redirect('home')
    
def add_OrderDetails(request):
    order_form = AddOrderRecordForm(request.POST or None) 
    if request.user.is_authenticated:
        if request.method == "POST":
            if order_form.is_valid():
                add_OrderDetails = order_form.save()
                messages.success(request, _("Details added successfully!!..."))
                return redirect('/')
        return render(request, 'add_OrderDetails.html', {'order_form':order_form})
    else:
        messages.success(request, _("You must be logged in to add a form"))
        return redirect('home')
    
def add_OrderSpecs(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            order_specs_form = AddOrderSpecsForm(request.POST)
            if order_specs_form.is_valid():
                order_specs_form.save()
                messages.success(request, _("Specifications added successfully!!..."))
                return redirect('/')
        else:
            order_specs_form = AddOrderSpecsForm()  # Initialize the form for GET requests
        
        return render(request, 'add_OrderSpecs.html', {'order_specs_form': order_specs_form})
    else:
        messages.success(request, _("You must be logged in to add a form"))
        return redirect('home')

 