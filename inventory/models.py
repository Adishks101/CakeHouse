from django.db import models

from franchise.models import Franchise
from product.models import Product


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    available_quantity = models.PositiveIntegerField()
    total_sold = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventory for {self.product.name}"

    def update_available_quantity(self, quantity_sold):
        print(self.available_quantity)
        self.total_sold += quantity_sold
        self.available_quantity -= quantity_sold
        print(self.available_quantity)

        self.save()
