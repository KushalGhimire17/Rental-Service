from django.urls import path
from .views import ProductDetail, ProductList, BookProductList, BookProductDetail, CategoryList, CategoryDetail

urlpatterns = [
    path('',ProductList.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetail.as_view(), name='product-detail'),

    path('bookproducts/',BookProductList.as_view(), name='book-product-list'),
    path('bookproducts/<int:pk>/', BookProductDetail.as_view(), name='book-product-detail'),

    
    path('category/',CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
]