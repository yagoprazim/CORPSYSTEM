from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from api.views.client import ClientViewSet
from api.views.vendor import VendorViewSet, UserVendorDetailView
from api.views.product import ProductGroupViewSet, ProductViewSet
from api.views.sale import SaleItemViewSet, SaleViewSet, PaymentMethodChoicesView
from api.views.authentication import LoginView, LogoutAPIView
from api.views.report import ExportSalesToCSVView, ExportSalesToPDFView

router = routers.DefaultRouter()
router.register('clients', ClientViewSet, basename='clients')
router.register('vendors', VendorViewSet, basename='vendors')
router.register('product-groups', ProductGroupViewSet, basename='product-groups')
router.register('products', ProductViewSet, basename='products')
router.register('sale-items', SaleItemViewSet, basename='sale-items')
router.register('sales', SaleViewSet, basename='sales')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView().as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()), 
    path('user/vendor/', UserVendorDetailView.as_view(), name='vendor-detail'),
    path('payment-methods/', PaymentMethodChoicesView.as_view(), name='payment-method-choices'),
    path('export_sales/csv/', ExportSalesToCSVView.as_view(), name='export_sales_to_csv'),
    path('export_sales/pdf/', ExportSalesToPDFView.as_view(), name='export_sales_to_pdf'),
]
