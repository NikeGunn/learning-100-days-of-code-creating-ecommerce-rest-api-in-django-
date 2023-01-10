from rest_framework import serializers
from decimal import Decimal

from store.models import Product
from store.models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only = True)




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','slug', 'description', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    
    
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    #Long way using Serializers

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length = 255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price')
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name= 'collection-detail'

    #Using ModelSerializers with Meta class & it is the shortcut way
