from django.contrib import admin
from .models import ItemRate,PickupRequest,PickupRequestItem

# Register your models here.
admin.site.register(ItemRate)
admin.site.register(PickupRequest)
admin.site.register(PickupRequestItem)
