from django import forms
from django.forms.fields import CharField 

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    phone = forms.CharField(max_length=255)
    address = forms.CharField(max_length=1000)
    pincode = forms.CharField(max_length=255)
    latitude = forms.CharField(max_length=255, required=False)
    longitude = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=255)
    payment_type = forms.CharField(max_length=255)