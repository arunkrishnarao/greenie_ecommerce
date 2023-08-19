from django.db import models

class Settings(models.Model):
    heading = models.CharField(max_length=200)
    subheading = models.CharField(max_length=500)
    facebook = models.CharField(max_length=500, default='https://www.facebook.com/')
    instagram = models.CharField(max_length=500, default='https://www.instagram.com/')
    twitter = models.CharField(max_length=500, default='https://www.twitter.com/')
    shipping_cost = models.FloatField(default=50.0)
    email = models.CharField(max_length=500, default='')