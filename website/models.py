from django.db import models

# Create your models here.
class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=5)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return(f"{self.name}")
    
class Order(models.Model):
    order_id = models.CharField(max_length=5, default='00000')
    STATUS = (
            ('Pending', 'Pending'),
            ('Ready for dispatch', 'Ready for dispatch'),
            ('Out for delivery', 'Out for delivery'),
            ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000, default='Default description')
    status = models.CharField(max_length=200, choices=STATUS, default='Pending') 

    def __str__(self):
        return f"Order {self.order_id} for {self.customer.name}"

class OrderSpecs(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderspecs')
    article = models.CharField(max_length=25)
    pieces = models.IntegerField(default=1)  # whole number
    material = models.CharField(max_length=50, default='default material')
    length = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)  # decimal for measurements
    breadth = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    thickness = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    quantity = models.IntegerField(default=1)  # whole number
    pricePerMeter = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)  # decimal for currency

    def __str__(self):
        return f"Order {self.id} for {self.order.customer.name}"

    def total_price(self):
        # Example method to calculate the total price
        return self.quantity * self.length * self.pricePerMeter