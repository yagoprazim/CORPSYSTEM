from rest_framework import serializers
from api.models.sale import SaleItem, Sale

class SaleItemSerializer(serializers.ModelSerializer):
    product_info = serializers.SerializerMethodField()

    class Meta:
        model = SaleItem
        fields = ['id', 'sale', 'product', 'product_info', 'quantity', 'total_price']
        read_only_fields = ['total_price']
    
    def get_product_info(self, obj):
        return {
            'name': obj.product.name
        }

    def validate(self, data):
        sale = data.get('sale')
        product = data.get('product')
        quantity = data.get('quantity')

        if sale.is_finalized:
            raise serializers.ValidationError("Cannot add items to a finalized sale.")
        
        if quantity > product.stock:
            raise serializers.ValidationError("Quantity exceeds available stock.")
        
        return data

    def create(self, validated_data):
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        product.stock -= quantity
        product.save()

        return super().create(validated_data)
    
class SaleSerializer(serializers.ModelSerializer):
    client_info = serializers.SerializerMethodField()
    vendor_info = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'client', 'client_info', 'vendor', 'vendor_info', 'payment_method', 'total_amount', 'date', 'is_finalized']
        read_only_fields = ['vendor']

    def get_client_info(self, obj):
        return {
            'name': obj.client.name,
            'cpf': obj.client.cpf
        }

    def get_vendor_info(self, obj):
        return {
            'name': obj.vendor.name,
            'credential_code': obj.vendor.credential_code
        }
    
    def get_total_amount(self, obj):
        return obj.total_amount
