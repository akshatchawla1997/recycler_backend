from django.urls import include, path
from rest_framework import routers
from .views.AdminLoginView import AdminLoginView
from .views.LoginView import LoginView
from .views.LogoutView import LogoutAPIView
from .views.UserUpdateView import UserUpdateView
from .views.VendorLoginView import VendorLoginView
from .views.VendorSignupView import VendorSignupView
from .views.CustomerPickupDetailsView import CustomerPickupDetails
from .views.CountUsersAndVendorView import CountUsersAndVendor
from .views.VendorsReportView import VendorReportView
router = routers.DefaultRouter()
router.register(r'vendors', VendorSignupView, basename='vendor')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),    
    path('update-user/', UserUpdateView.as_view({'put': 'update'}), name='update-user'),
    path('admin-login/', AdminLoginView.as_view(), name='admin-login'),
    path('vendor-login/',VendorLoginView.as_view(),name='vendor'),
    path('customer-pickup-details/<int:userid>', CustomerPickupDetails.as_view(), name='CustomerPickupDetails'),
    path('api/', include(router.urls)),
    path('count/', CountUsersAndVendor.as_view()),
    path('vendor/',VendorReportView.as_view())
]
urlpatterns += router.urls
