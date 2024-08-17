from django.db import models
from api.models.client import Client
from api.models.vendor import Vendor
from api.models.product import Product

class Sale(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CC', 'Credit Card'),
        ('DC', 'Debit Card'),
        ('CA', 'Cash'),
        ('PIX', 'Pix'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=3, choices=PAYMENT_METHOD_CHOICES, default='CA')
    date = models.DateField(auto_now_add=True)
    is_finalized = models.BooleanField(default=False)

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())
    
    def __str__(self):
        return f"Client: {self.client.name} - Vendor: {self.vendor.name} - Is_finalized: {self.is_finalized}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"