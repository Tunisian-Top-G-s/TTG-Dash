from datetime import timezone
from django.db import models
from Users.models import Address, CustomUser
from Products.models import Product
# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )
    
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    SHIPPING = (
        (0, 'Pick up in store'),
        (1, 'Ship to home'),
    )
    
    shippingMethod = models.CharField(max_length=20, choices=SHIPPING, default=1)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders', null=True)  # Address field added

    PAYMENT_METHODS = (
        ('cash', 'Cash on Delivery'),
        ('credit_card', 'Credit Card'),
        # Add more payment methods as needed
    )

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')  # Payment method field added

    def calculate_total_price(self):
        total = sum(item.product.price * item.quantity for item in self.order_items.all())
        return total

    def __str__(self):
        return f"Order {self.id} for {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    types = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in Order"