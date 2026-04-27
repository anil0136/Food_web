from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class multivendors(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    restaurant_name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zip_code=models.CharField(max_length=10)
    restaurant_lic=models.ImageField(upload_to='licience_pics/',blank=True,null=True)
    restaurant_img=models.ImageField(upload_to='restaurent_pics/',blank=True,null=True)
    user_type =models.CharField(max_length=100,default="vendor",editable=False)
    is_approved=models.BooleanField(default=False,editable=True)
    Franchise=models.BooleanField(default=False)

    def __str__(self):
        return self.restaurant_name

class menubuilding(models.Model):
    ver=models.ForeignKey(multivendors,related_name="multivendorss",on_delete=models.CASCADE)
    
    food_name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    food_img =models.ImageField(upload_to='food_img/',blank=True,null=True)

    def __str__(self):
        return self.food_name


class Franchise(models.Model):
    vendor = models.ForeignKey(multivendors, related_name="franchises", on_delete=models.CASCADE)
    total_investment = models.PositiveIntegerField()
    total_year_of_aggr = models.PositiveIntegerField()
    profit_share = models.PositiveIntegerField()
    description = models.TextField(max_length=100)
    
    def __str__(self):
        return f"{self.vendor.restaurant_name} franchise"


class FranchiseOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="franchise_orders")
    vendor = models.ForeignKey(multivendors, on_delete=models.CASCADE, related_name="franchise_orders_received")
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.vendor.restaurant_name}"
    


