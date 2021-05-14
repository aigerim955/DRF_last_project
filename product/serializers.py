from rest_framework import serializers

from .models import Category, Product, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'image')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),write_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


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


class CreateUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'categories']

