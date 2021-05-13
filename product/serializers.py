from rest_framework import serializers

from product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'image')


class ProductSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='post-detail',
                                                   lookup_field='slug')

    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='post-detail',
                                                   lookup_field='slug')
    class Meta:
        model = Product
        fields = ('title', 'slug', 'image', 'created_at', 'details')
