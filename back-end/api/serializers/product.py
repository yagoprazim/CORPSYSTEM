from rest_framework import serializers
from api.models.product import ProductGroup, Product

class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    group_info = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'group', 'group_info']

    def get_group_info(self, obj):
        return {
            'name': obj.group.name
        }
