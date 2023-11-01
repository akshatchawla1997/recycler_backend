from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views.UserViewSet import UserViewSet

router = DefaultRouter()
router.register("user", UserViewSet, basename="user")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('transactions/', include('transactions.urls'))
    ]
urlpatterns += router.urls