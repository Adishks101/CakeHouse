from django.db import models

from franchise.models import Franchise
from product.models import Product


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    franchise=models.ForeignKey(Franchise, on_delete=models.CASCADE)
    available_quantity = models.PositiveIntegerField()
    total_sold = models.PositiveIntegerField(default=0)  # New field to track total quantity sold
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventory for {self.product.name}"

    def update_total_sold(self, quantity_sold):
        self.total_sold += quantity_sold
        self.save()
