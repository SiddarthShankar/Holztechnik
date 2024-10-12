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
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=200, choices=STATUS)
    
    def __str__(self):
        return f"Order {self.id} for {self.customer.name}"