from django.db import models

# Create your models here.

class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, primary_key=True)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='posts')
    image = models.ImageField(upload_to='posts/')
    created_at = models.DateTimeField(auto_now_add=True)


class ProductImage(models.Model):
    pass

class Review(models.Model):
    pass



