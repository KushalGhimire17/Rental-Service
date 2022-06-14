
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes


from .serializers import ProductSerializer, ProductMultipleImageSerializer, CategorySerializer, BookProductSerializer

from .permissions import IsAuthorOrReadOnly, IsAdminUserOrReadOnly

from .models import Product, ProductMultipleImage, Category, BookProduct

from django.http import HttpResponse




class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_posted=True)
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            return HttpResponse('<p>Create a free account to post !</p>')

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]



class BookProductList(generics.ListCreateAPIView):
    queryset = BookProduct.objects.all()
    serializer_class = BookProductSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]


class BookProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookProduct.objects.all()
    serializer_class = BookProductSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]