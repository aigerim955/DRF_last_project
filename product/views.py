from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions as p, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import ProductFilter
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer, CreateUpdateProductSerializer
from .models import Category, Product, Comment


class MyPagination(PageNumberPagination):
    page_size = 2

    # def get_paginated_response(self, data):
    #     for i in range(self.page_size):
    #         text = data[1]['text']
    #         data[1]['text'] = text[:15] + '...'
    #     return super().get_paginated_response(data)


class CategoriesList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [AllowAny, ]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = ProductFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductSerializer
        return CreateUpdateProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retreiver', 'search']:
            permissions = [p.AllowAny]
        else:
            permissions = [p.IsAdminUser]
        return [permissions() for permissions in permissions]

    @action(methods=['GET'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [p.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

