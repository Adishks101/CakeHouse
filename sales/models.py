from django.db import models
from django.contrib.auth import get_user_model
from customer.models import Customer

from franchise.models import Franchise
from product.models import Product

User = get_user_model()


class Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    PAYMENT_MODE = (
        ('cash', 'Cash'),
        ('bank', 'Bank'),
    )
    payment_mode = models.CharField(max_length=4, choices=PAYMENT_MODE, default='cash')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sale of {self.product.name} by {self.user.username}"


class SaleItem(models.Model):
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
