from django.conf.urls.static import static
from django.urls import include, path
from transactions.views import BankDetailsView,WalletViewSet, WalletDetailView, WalletHistoryViewSet,UserAndWalletView,CustomerReportView
from rest_framework import routers
from recycler import settings

router = routers.DefaultRouter()
router.register(r'wallet', WalletViewSet)

urlpatterns =[
    path('bank-details/',BankDetailsView.as_view({'get':'list','post':'create'})),
    path('',include(router.urls)),
    path('wallet/<int:pk>/', WalletDetailView.as_view()),
    path('wallet-history/', WalletHistoryViewSet.as_view({'get':'list','post':'create'}), name="wallet History"),
    path('wallet-history/get_history_by_wallet_id/', WalletHistoryViewSet.as_view({'get': 'get_history_by_wallet_id'})),
    path('wallet-details/',UserAndWalletView.as_view()),
    path('customer-report/',CustomerReportView.as_view())
]