from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from orders.views import PickupRequestViewSet
from recycler import settings
from .views import ItemRateViewSet, PickupRequestItemView, AppPickupHistoryData, CreateAndUpdateCartView, OrderRequestItemView, OrderRequestViewSet,UserTransactionDetailsView, VerifyPickupOTPView,AddToCartView,  UserPickupViewSet



router = routers.DefaultRouter()
router.register(r'pickup-requests/(?P<user>\d+)', PickupRequestViewSet)
router.register(r'pickup-requests', PickupRequestViewSet, basename='pickup-requests')

urlpatterns = [
    path('item-rates/', ItemRateViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('order/', OrderRequestViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('item-rates/<int:pk>/', ItemRateViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('order/<int:pk>/', OrderRequestViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('api/', include(router.urls)),
    path('order/vendor-details/<int:vendor_id>/',OrderRequestItemView.as_view(), name='my-view'),
    path('', PickupRequestItemView.as_view()),
    path('<int:order_id>/verify-otp/',VerifyPickupOTPView.as_view(), name='verify_pickup_otp'),
    path('customer-details/',UserPickupViewSet.as_view(), name='customer_details'),
    path('Transaction/', UserTransactionDetailsView.as_view({'get': 'list', 'post': 'create'}), name='customer_transaction'),
    path('app/add-to-cart/<int:user_id>/', AddToCartView.as_view({'get': 'list' }), name='add_to_cart'),
    path('app/add-to-cart/',AddToCartView.as_view({'post':'create', 'delete': 'destroy'}), name='add_to_cart'),
    path('app/update-cart/<int:pk>/', AddToCartView.as_view({'patch': 'partial_update' }), name='add_to_cart'),
    path('app/add_or_update_cart/', CreateAndUpdateCartView.as_view(), name='create_update_cart'),
    path('app/pickup_history/<int:user_id>/', AppPickupHistoryData.as_view(), name='pickup_history'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



