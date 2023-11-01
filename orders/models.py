from django.db import models
from accounts.models import UserModel

# Create your models here.
class ItemRate(models.Model):
    item_name = models.CharField(max_length=100)
    rate = models.TextField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.item_name


class PickupRequest(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    items = models.ManyToManyField(ItemRate, through='PickupRequestItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    flat_number = models.TextField()
    area = models.TextField()
    landmark = models.TextField(null=True, blank=True)
    city = models.TextField()
    state = models.TextField()
    pincode = models.CharField(max_length=6)
    status_choices = [("requested","Requested"),("completed","Completed")]
    status = models.CharField(max_length=100, choices=status_choices, default="requested")

    def __str__(self):
        return f"Pickup Request - {self.user.username} - {self.items.name}"

class PickupRequestItem(models.Model):
    pickup_request = models.ForeignKey(PickupRequest, on_delete=models.CASCADE)
    item_id = models.ForeignKey(ItemRate, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Pickup Request Item - {self.item_rate.item_name}"
    
class MyCartItems(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item_id = models.ForeignKey(ItemRate, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ('user', 'item_id')

class Orders(models.Model):
    pickup_id = models.ForeignKey(PickupRequest, on_delete=models.CASCADE, related_name='pickup_id')
    vendor_id = models.ForeignKey(UserModel, on_delete=models.CASCADE,  limit_choices_to = {'is_vendor': True})
    category = models.ManyToManyField(ItemRate, through='OrderItems')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_proof = models.ImageField(upload_to='images/',null=True, blank=True)
    total_amount = models.IntegerField(default=0)
    status_choices = [("live", "Live"), ("onhold", "On Hold"),("completed", "Completed"),("rejected", "Rejected"),("picked","Picked"),("paid","Paid")]
    order_status = models.CharField(max_length=100, choices=status_choices, default="onhold")
    

class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, blank=True)
    item_id = models.ForeignKey(ItemRate, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=10)

class UserTransactionDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, blank=True)
    transactionId = models.TextField()
    userId = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    total_amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  