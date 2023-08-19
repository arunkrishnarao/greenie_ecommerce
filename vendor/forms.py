from django.forms import ModelForm, models
from product.models import Product, Vendor

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price']

class ProductEditForm(ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'description']
    
    def __init__(self, *args, **kwargs):
        super(ProductEditForm, self).__init__(*args, **kwargs)

class VendorEditForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['image', 'name', 'email', 'address', 'phone']
    def __init__(self, *args, **kwargs):
        super(VendorEditForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['name'].required = False
        self.fields['email'].required = False
        self.fields['address'].required = False
        self.fields['phone'].required = False