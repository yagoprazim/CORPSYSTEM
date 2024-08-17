from django.db import transaction
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models.sale import SaleItem, Sale
from api.serializers.sale import SaleItemSerializer, SaleSerializer
from api.permissions.permissions import IsVendor

class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAuthenticated, IsVendor]

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        sale = instance.sale
        product = instance.product
        quantity = instance.quantity

        if sale.is_finalized:
            return Response({'error': 'Cannot delete a sale item from a finalized sale.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        product.stock += quantity
        product.save()

        return super().destroy(request, *args, **kwargs)

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, IsVendor]

    def perform_create(self, serializer):
        vendor = self.request.user.vendor
        serializer.save(vendor=vendor)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        sale_items = instance.items.all()
        
        if instance.is_finalized:
            return Response({'error': 'Cannot delete a finalized sale.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        for item in sale_items:
            product = item.product
            product.stock += item.quantity
            product.save()
        
        sale_items.delete()
        
        return super().destroy(request, *args, **kwargs)

class PaymentMethodChoicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        choices = Sale.PAYMENT_METHOD_CHOICES
        payment_methods = [{'value': value, 'label': label} for value, label in choices]
        return Response({'payment_methods': payment_methods})