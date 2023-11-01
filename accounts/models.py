from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    # Group,
    PermissionsMixin,
)
from django.core.validators import RegexValidator, validate_email
from django.db import models


phone_regex = RegexValidator(
    regex=r"^\d{10}", message="Phone number must be 10 digits only."
)

class UserManager(BaseUserManager):
    """
    User Manager.
    To create superuser.
    """
    def create_user(self, phone_number):
        if not phone_number:
            raise ValueError("Users must have a phone_number")
        user = self.model(phone_number=phone_number)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(phone_number)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_vendor(self,phone_number,password = None,pincode=None):
        user = self.create_user(phone_number)
        user.is_active = True
        user.is_staff = True
        user.is_vendor = True
        user.set_password(password)
        user.save(using=self._db)
class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model.
    """
    phone_number = models.CharField(
        unique=True, max_length=10, null=False, blank=False, validators=[phone_regex]
    )
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        validators=[validate_email],
    )
    otp = models.CharField(max_length=6)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_registered_at = models.DateTimeField(auto_now_add=True)
    is_vendor = models.BooleanField(default=False)
    vendor_status_choices = [("allocated","Allocated"),("not_allocated","Not Allocated"),]
    vendor_status = models.CharField(max_length=100, choices=vendor_status_choices, default="not_allocated")
    pincode = models.CharField(max_length=6,null=True)
    upiId = models.TextField(blank=True, null=True)
    pickup_otp = models.CharField(max_length=4, null=True, blank=True)
    USERNAME_FIELD = "phone_number"
    objects = UserManager()
    def __str__(self):
        return self.phone_number
 
class APILog(models.Model):
    request_method = models.CharField(max_length=10)
    request_path = models.CharField(max_length=255)
    request_headers = models.TextField()
    request_body = models.TextField()
    request_data = models.TextField()
    response_status = models.IntegerField(default=200, null=True)
    response_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request_method} {self.request_path}"
