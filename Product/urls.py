from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryView, ProductView


router = DefaultRouter()
router.register(r'categories', CategoryView, basename='category')
router.register(r'products', ProductView, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
