from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)

    def __str__(self):
        return f"Order {self.order_id} for {self.customer.name}"

class OrderSpecs(models.Model):
    id = models.BigAutoField(primary_key=True)  # Primary key
    order_spec_id = models.CharField(max_length=5, default='00000', unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderspecs')
    article = models.CharField(max_length=25)
    pieces = models.IntegerField(default=1)  # whole number
    material = models.CharField(max_length=50, default='default material')
    length = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)  # decimal for measurements
    breadth = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    thickness = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    quantity = models.IntegerField(default=1)  # whole number
    pricePerMeter = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)  # decimal for currency

class Picking(models.Model):
    item_to_pick = models.CharField(max_length=255)  # The item to pick
    article_id = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    stock_quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])  # The quantity available in stock
    
    def __str__(self):
        return f"Picking {self.item_to_pick}, Article ID: {self.article_id}, {self.stock_quantity} in stock"

class PickingList(models.Model):
    orderspec = models.ForeignKey(OrderSpecs, on_delete=models.CASCADE, null=False, related_name='picking_lists')
    picking = models.ForeignKey(Picking, on_delete=models.CASCADE, related_name='picking_lists')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Picking List for {self.orderspec}"
    
class LedMapping(models.Model):
    led_index = models.PositiveIntegerField(unique=True)
    article_id = models.PositiveIntegerField()

    def __str__(self):
        return f"LED {self.led_index} -> Article {self.article_id}"

    class Meta:
        db_table = "led_mapping"  # Explicitly set the table name
