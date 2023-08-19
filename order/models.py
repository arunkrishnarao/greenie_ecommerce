from email.policy import default
from django.db import models
from product.models import Product
from vendor.models import Vendor

class PaymentStatus:
    SUCCESS = "Success"
    FAILURE = "Failure"
    PENDING = "Pending"
    CANCELLED = "Cancelled"

# Create your models here.
class Order(models.Model):
    full_name = models.CharField(max_length=255, default = "")
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=1000)
    pincode = models.CharField(max_length=255, default = "")
    latitude = models.CharField(max_length=255, default = "")
    longitude = models.CharField(max_length=255, default = "")
    city = models.CharField(max_length=255, default="Mysuru")
    amount = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False, default=0)
    status =  models.CharField(default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )

    payment_info = models.CharField(max_length=255, default="COD")
    created_at = models.DateTimeField(auto_now_add=True)
    vendors = models.ManyToManyField(Vendor, related_name="orders")

    provider_order_id = models.CharField(max_length=40, default="COD")
    payment_id = models.CharField(max_length=36, default="COD")
    signature_id = models.CharField(max_length=128, default="COD")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name="items", on_delete=models.CASCADE)
    vendor_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        return self.price * self.quantity
