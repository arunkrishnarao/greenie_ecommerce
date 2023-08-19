from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import OneToOneField
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.db.models import Q

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='./', blank=True, null=True)
    active = models.BooleanField(default=False)
    email = models.CharField(max_length=1024, default='')
    address = models.CharField(max_length=2048, default='')
    phone = models.CharField(max_length=255, default='')
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True) # Change uploads to thumbnails 

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                # Default Image
                return 'https://via.placeholder.com/240x180.jpg'
    
    # Generating Thumbnail - Thumbnail is created when get_thumbnail is called
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id]).exclude(Q(order__status="Cancelled"))
        return sum((item.product.price * item.quantity) for item in items)

    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)