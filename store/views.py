from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from .models import Product, Collection, OrderItem
from .serializers import ProductSerializer
from .serializers import CollectionSerializer

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        # if Product.objects.filter(kwargs=['pk']).count() > 0:
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Because of related fields cannet be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)

        # if product.orderitem_set.count() > 0:
        #     return Response({'error': 'Product cannot be deleted because it is associated to orderitems'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
        # product.delete()
        # return Response({'deleted': 'Successfully Deleted'}, status=status.HTTP_204_NO_CONTENT)  

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer



    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'These collections cannot be deleted because it included one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().destroy(request, *args, **kwargs)




