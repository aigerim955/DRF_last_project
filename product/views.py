from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions as p, generics
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer
from .models import Category, Product, Comment


class MyPagination(PageNumberPagination):
    page_size = 1


class CategoriesList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = MyPagination


class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [p.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

