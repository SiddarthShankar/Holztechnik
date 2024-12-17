from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Order, OrderSpecs
from .filters import OrderFilter, CustomerFilter
from django.utils.translation import gettext as _
from collections import defaultdict
from .forms import *
import subprocess

@csrf_exempt

def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    myFilters = CustomerFilter(request.GET, queryset=customers)
    customers = myFilters.qs
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'customers': customers, 'orders': orders, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending, 'myFilters': myFilters}
                
    # Check if logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authentication step
        user = authenticate(request, username=username, password=password)
        print(user)
        if user.username == "Vorgesetzter":
            login(request, user)
            messages.success(request, _("You have been successfully logged in!"))
            return redirect('home')  # Redirect after successful login
        elif user.username == "Endfertigungteckniker":
            login(request, user)
            messages.success(request, _("Please enter order_id..."))
            return redirect('enter_order_id')
        else:
            messages.error(request, _("Invalid credentials, please try again."))
            return render(request, 'home.html', context)
        
    # Render the page for GET requests
    return render(request, 'home.html', context)
    
def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, _("You have been successfully Logged Out!!...."))
    return redirect('home')

def about(request):
    if request.user.is_authenticated:
        if request.user.username == "Vorgesetzter":
            return render(request, 'about.html', {'about':about})
        else:
            messages.error(request, _("Access denied!!"))
            return redirect('enter_order_id')
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
        if request.user.username == "Vorgesetzter":
            if request.method == "POST":
                if customer_form.is_valid():
                    add_CustomerDetails = customer_form.save()
                    messages.success(request, _("Details added successfully!!..."))
                    return redirect('home')
            return render(request, 'add_CustomerDetails.html', {'customer_form':customer_form})
        else:
            messages.error(request, _("Access denied!!"))
            return redirect('enter_order_id')
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

def order(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, pk=order_id)
        orderspecs = order.orderspecs.all()
        context = {
            'order': order,
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
        if request.user.username == "Vorgesetzter":
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
            messages.error(request, _("Access denied!!"))
            return redirect('enter_order_id')
    else:
        messages.success(request, _("You must be logged in to add a form"))
        return redirect('home')

def delete_OrderDetails(request, pk):
    if request.user.is_authenticated:
        if request.user.username == "Vorgesetzter":
            delete_detail = Order.objects.get(id=pk)
            delete_detail.delete()
            messages.success(request, _("Details have been deleted successfully!!.."))
            return redirect('home') 
        else:
            messages.error(request, _("Access denied!!"))
            return redirect('enter_order_id')
    else:
        messages.success(request, _("You must be logged into access the data"))
        return redirect('home') 
    
def update_OrderDetails(request, pk):
    if request.user.is_authenticated:
        if request.user.username == "Vorgesetzter":
            current_detail = Order.objects.get(id=pk)
            order_form = AddOrderRecordForm(request.POST or None, instance=current_detail)
            if order_form.is_valid():
                order_form.save() 
                messages.success(request, _("Details have been Updated successfully!!.."))
                return redirect('home') 
            return render(request, 'update_OrderDetails.html', {'order_form':order_form})
        else:
            messages.error(request, _("Access denied!!"))
            return redirect('enter_order_id')
    else:
        messages.success(request, _("You must be logged into access the data"))
        return redirect('home') 
      
def update_OrderSpecs(request, pk):
    if request.user.is_authenticated:
        current_detail = OrderSpecs.objects.get(id=pk)
        orderspecs_form = AddOrderSpecsForm(request.POST or None, instance=current_detail)
        if orderspecs_form.is_valid():
            orderspecs_form.save() 
            messages.success(request, _("Details have been Updated successfully!!.."))
            return redirect('home') 
        return render(request, 'update_OrderSpecs.html', {'orderspecs_form':orderspecs_form})
    else:
        messages.success(request, _("You must be logged into access the data"))
        return redirect('home') 
    
def enter_order_id(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')

        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                return redirect('order', order_id=order_id)
            except Order.DoesNotExist:
                messages.error(request, _("Order ID does not exist."))
                return redirect('enter_order_id') 
        else:
            messages.error(request, _("Please enter a valid Order ID."))
    return render(request, 'enter_order_id.html') 

def picking_list(request, order_spec_id):
    # Retrieve the specific OrderSpecs object
    order_spec = get_object_or_404(OrderSpecs, pk=order_spec_id)
    
    # Get the associated order_id
    order_id = order_spec.order.id
    
    # Fetch all related OrderSpecs for the given order_id
    related_order_specs = OrderSpecs.objects.filter(order_id=order_id)
    
    # Fetch PickingList entries for these related OrderSpecs
    picking_lists = PickingList.objects.filter(orderspec__in=related_order_specs)
    
    # Group PickingList entries by orderspec_id and include order_id in the context
    grouped_pickings = defaultdict(list)
    for picking_list in picking_lists:
        grouped_pickings[picking_list.orderspec.id].append(picking_list)
    
    # Prepare the context
    context = {
        'order_spec': order_spec,                     # The specific OrderSpec being viewed
        'order_id': order_id,                         # Associated order_id
        'grouped_pickings': dict(grouped_pickings),   # Grouped picking lists by orderspec_id
        'related_order_specs': related_order_specs,   # Related OrderSpecs for the same order_id
    }
    
    # Render the picking_list template
    return render(request, 'picking_list.html', context)


def picking_iterator(request, order_id):
    # Get the specific Order
    order = get_object_or_404(Order, pk=order_id)

    # Store the order_id in session for future use
    request.session['order_id'] = order_id

    # Initialize the picking list on the first load
    if 'picking_list' not in request.session:
        # Fetch all OrderSpecs related to the current order
        related_order_specs = OrderSpecs.objects.filter(order=order)

        # Fetch PickingList entries for all related OrderSpecs
        picking_lists = PickingList.objects.filter(orderspec__in=related_order_specs).select_related('picking')

        if not picking_lists.exists():
            messages.error(request, "No items found in the Picking List for this order.")
            return redirect('home')

        # Group PickingList entries by orderspec_id
        grouped_pickings = defaultdict(list)
        for picking_list in picking_lists:
            grouped_pickings[picking_list.orderspec.id].append({
                'picking_list': picking_list,
                'picking': picking_list.picking,
            })

        # Store the grouped picking list in session
        request.session['picking_list'] = {key: [
            {
                'id': entry['picking_list'].id,
                'article_id': entry['picking'].article_id,
                'item_to_pick': entry['picking'].item_to_pick,
                'quantity': entry['picking_list'].quantity,
                'stock_quantity': entry['picking'].stock_quantity,
            }
            for entry in entries
        ] for key, entries in grouped_pickings.items()}

        request.session['current_index'] = 0  # Start at the first item

    # Get the current index and picking list from the session
    current_index = request.session['current_index']
    picking_list = request.session['picking_list']

    # Flatten the picking list for iteration
    flat_picking_list = [
        item for items in picking_list.values() for item in items
    ]

    # Check if we still have items to iterate
    if current_index < len(flat_picking_list):
        current_picking = flat_picking_list[current_index]

        # Extract required fields
        article_id = current_picking['article_id']
        item_to_pick = current_picking['item_to_pick']
        quantity = current_picking['quantity']
        stock_quantity = current_picking['stock_quantity']

        # Check stock quantity before proceeding
        if stock_quantity < quantity:
            messages.error(request, f"Insufficient stock for {item_to_pick}. Required: {quantity}, Available: {stock_quantity}")
            request.session['current_index'] += 1
            return redirect('picking_iterator', order_id=order_id)

        # Reduce stock quantity
        updated_stock_quantity = stock_quantity - quantity
        current_picking['stock_quantity'] = updated_stock_quantity
        flat_picking_list[current_index] = current_picking  # Update session data

        # Update stock in the database
        Picking.objects.filter(article_id=article_id).update(stock_quantity=updated_stock_quantity)

        # Add warning message if stock quantity is below 15
        if updated_stock_quantity < 15:
            messages.warning(request, f"Warning: Stock for {item_to_pick} is low ({updated_stock_quantity} left).")

        # Handle LED lighting
        led_mapping = LedMapping.objects.filter(article_id=article_id).first()
        led_index = led_mapping.led_index if led_mapping else None

        if led_index is not None:
            try:
                subprocess.run(['python3', '/home/siddarthshankar/Desktop/led_control.py', str(led_index)], check=True)
            except Exception as e:
                print(f"Failed to light up LED {led_index} for article {article_id}: {e}")

        context = {
            'order': order,
            'picking': current_picking,
            'last_item': current_index == len(flat_picking_list) - 1,
            'led_index': led_index,
        }
    else:
        # Clear the session if the list is finished
        request.session.pop('picking_list', None)
        request.session.pop('current_index', None)
        context = {
            'order': order,
            'finished': True,  # Flag to indicate the picking process is finished
            'message': 'Picking List Completed',  # Message to show when finished
        }

    return render(request, 'picking_iterator.html', context)

def next_picking(request):
    # Increment the index for the next picking item
    if 'current_index' in request.session:
        request.session['current_index'] += 1

    # Retrieve the order_id from the session
    order_id = request.session.get('order_id')

    # Ensure the order_id is available for redirection
    if order_id:
        # Redirect to picking_iterator using order_id
        return redirect('picking_iterator', order_id=order_id)
    else:
        # Handle missing order_id in session
        messages.error(request, "Order ID not found in session.")
        return redirect('home')  # Fallback page if session data is missing
    
def add_picking_item(request):
    if request.user.is_authenticated:
        if request.user.username == "Vorgesetzter":
            if request.method == 'POST':
                Pickingitem = PickingItem(request.POST)
                if Pickingitem.is_valid():
                    Pickingitem = Pickingitem.save()
                    messages.success(request, "Picking item added successfully!")
                else:
                    messages.error(request, "Please correct the errors in the form.")
            else:
                Pickingitem = PickingItem()
            return render(request, 'add_picking_item.html', {'Pickingitem': Pickingitem})
        else:
            messages.error(request, _("Access denied! Only Vorgesetzter can add picking items."))
            return redirect('enter_order_id')  # Replace with a more appropriate redirect if necessary
    else:
        messages.error(request, _("You must be logged in to add picking items."))
        return redirect('home')

def create_picking(request, order_spec_id):
    if request.user.is_authenticated:
        if request.user.username == "Vorgesetzter":
            # Retrieve the specific OrderSpec
            order_spec = get_object_or_404(OrderSpecs, pk=order_spec_id)

            if request.method == 'POST':
                Pickingform = PickingForm(request.POST)
                if Pickingform.is_valid():
                    print(Pickingform.cleaned_data)
                    picking_list = Pickingform.save(commit=False)
                    picking_list.orderspec = order_spec  # Associate with the specific OrderSpec
                    picking_list.save()
                    messages.success(request, _("Picking list item added successfully!"))
                    return redirect('picking_list', order_spec_id=order_spec.id)
                else:
                    messages.error(request, _("Please correct the errors in the form."))
            else:
                Pickingform = PickingForm()

            return render(request, 'create_picking.html', {'Pickingform': Pickingform, 'order_spec': order_spec})
        else:
            messages.error(request, _("Access denied! Only Vorgesetzter can create picking items."))
            return redirect('home')  # Redirect to a suitable location
    else:
        messages.error(request, _("You must be logged in to create picking items."))
        return redirect('home')