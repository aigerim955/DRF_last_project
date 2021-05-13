from rest_framework.viewsets import ModelViewSet

from product.serializers import ProductSerializer
from product.models import Product


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_url_kwarg = 'slug'
    # filter_backends = [DjangoFilterBackend,
    #                    filters.SearchFilter,
    #                    filters.OrderingFilter]
    # filterset_fields = ['tags__slug', 'category']
    # search_fields = ['title', 'text', 'tags__title']
    # ordering_fields = ['created_at', 'title']
