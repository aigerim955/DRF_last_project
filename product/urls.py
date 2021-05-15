from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, CategoriesList, CommentCreate

router = DefaultRouter()
router.register('', ProductViewSet)

urlpatterns = [
    path('categories/', CategoriesList.as_view()),
    path('', include(router.urls)),
    # path('comments/', CommentCreate.as_view()),
]