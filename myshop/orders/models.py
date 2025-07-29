from django.db import models
from shop.models import Product

# Create your models here.

class Order(models.Model):
    """
    Represents an order in the system.
    Contains information about the products ordered, their quantities, and the total price.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f"Order {self.id}"
    
    def get_total_cost(self):
        """
        Calculate the total cost of the order.
        This method sums up the price of each product multiplied by its quantity.
        """
        return sum(item.get_cost() for item in self.items.all())
    
class OrderItem(models.Model):
    """
    Represents an item in an order.
    Contains information about the product, its quantity, and the order it belongs to.
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}"

    def get_cost(self):
        """
        Calculate the cost of this order item.
        This method multiplies the product's price by its quantity.
        """
        return self.price * self.quantity
