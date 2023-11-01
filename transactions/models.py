from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    # Group,
    PermissionsMixin,
)
from accounts.models import UserModel
from orders.models import Orders

class BankDetails(models.Model):
    account_number = models.BigIntegerField()
    ifsc_code = models.TextField()
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    account_holder_name = models.CharField(max_length=100)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.account_holder_name}'s Bank Details"

class BankHistory(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    transaction_id = models.AutoField(primary_key=True)
    refrence_id = models.IntegerField()
    status_choices = [("success", "Success"),("failed", "failed")]
    status = models.CharField(choices=status_choices, max_length=100, default="null")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.status()}"
    
class Wallet(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    wallet_amount = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Wallet of {self.user.name}"

class WalletHistory(models.Model):
    transaction_choices = [("dr","Dr"), ("cr","Cr")]
    transaction_type = models.CharField(max_length=100, choices=transaction_choices, default="null")
    transaction_amount =  models.DecimalField(max_digits=8, decimal_places=2,default=0)
    description_choices = [("redeemed","Redeemed"),("credited","Credited")]
    description = models.CharField(max_length=100, choices=description_choices, default="null")
    wallet_updated = models.DateTimeField(auto_now=True)
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE,  null=True)
    transaction_id = models.IntegerField( null=True)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.description}"
    
class PayContact(models.Model):
    name = models.TextField()
    email = models.CharField(max_length=100, null=True)
    contact = models.IntegerField()
    type = models.TextField(default='customer')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_id')
    refrence_id = models.IntegerField(unique=True)

    def __str__(self):
        return f"contact of {self.name()}"
