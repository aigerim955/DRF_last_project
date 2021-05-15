
# Create your models here.
import uuid
from time import time

from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify


def gen_slug(s):
    slug = slugify(s)
    return slug + '-' + str(int(time()))

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

    def save(self):
        if not self.slug:
            self.slug = gen_slug(self.name)
        super().save()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, blank=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    categories = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('price',)


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product,
                                related_name='images',
                                on_delete=models.CASCADE)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=400)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review was made by {self.author} on {self.product}, created at {self.created_at}.'


