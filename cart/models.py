from django.db import models
from vendors.models import menubuilding
from django.contrib.auth.models import User

# Create your models here.

class Cart(models.Model):
    fooditem=models.ForeignKey(menubuilding,related_name="menubuildings",on_delete=models.CASCADE)
    user=models.ForeignKey(User, related_name='carts', on_delete=models.CASCADE)
    Qty=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.fooditem.food_name} x {self.Qty}"

class Order(models.Model):
    PAYMENT_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('upi', 'UPI'),
        ('card', 'Card'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    food_item = models.ForeignKey(menubuilding, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.food_item.food_name} ({self.qty})"    
    
