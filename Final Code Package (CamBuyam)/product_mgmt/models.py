from django.db import models
from account_mgmt.models import *


class Market(models.Model):
      market_name = models.CharField( max_length=100)
      market_location = models.CharField( max_length=100)
      gmap_location_link =   models.CharField( max_length=1000, null=True)    


class Store(models.Model):
      seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True)
      shed_number = models.CharField(default="", max_length=15)
      market_id = models.ForeignKey(Market, on_delete=models.CASCADE,)
      store_name = models.CharField( max_length=100)
      store_location = models.CharField( max_length=100) 
      gmap_location_link =   models.CharField( max_length=1000, null=True)    


class Product(models.Model):
      photo = models.ImageField(upload_to='product_photos/', null=True, blank=False)
      product_name = models.CharField( max_length=100)
      price = models.DecimalField(max_digits = 15, decimal_places=2)
      quantity = models.IntegerField()
      description = models.CharField( max_length=100)
      category = models.CharField(max_length=100)
      measurement_unit = models.CharField( max_length=100)
      seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True)
      approved_by = models.ForeignKey(CustomAdmin, on_delete=models.CASCADE, null=True)
      approval_status =  models.CharField(default="unverified", max_length=20)
      store = models.ForeignKey(Store, on_delete=models.CASCADE)
      uploaded_at = models.DateField(auto_now_add = True, null=True, blank=True)



