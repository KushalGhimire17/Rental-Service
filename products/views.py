
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes


from .serializers import ProductSerializer, CategorySerializer, BookProductSerializer, MessageSerializer, CompanySerializer, ProductMultipleImageSerializer

from .permissions import IsAuthorOrReadOnly, IsAdminUserOrReadOnly

from .models import Product, ProductMultipleImage, Category, BookProduct, Message, Company, ProductOverview

from django.http import HttpResponse

from rest_framework.filters import SearchFilter

from django.http import JsonResponse

from itertools import groupby
from django.db.models import Q


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_posted=True)
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'price', 'location']
    authentication_classes = [TokenAuthentication,
                              SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            return HttpResponse('<p>Create a free account to post !</p>')


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_posted=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class FeaturedProductList(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_featured=True)
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication,
                              SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            return HttpResponse('<p>Create a free account to post !</p>')


class FeaturedProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_featured=True)
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


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class ProductGalleryList(generics.ListCreateAPIView):
    queryset = ProductMultipleImage.objects.all()
    serializer_class = ProductMultipleImageSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]


class ProductGalleryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductMultipleImage.objects.all()
    serializer_class = ProductMultipleImageSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


def getImageFullPath(image):
    url = "http://localhost:8000/media/" + image
    return url


def getProductDetail(request, id):
    products = list(Product.objects.values("id", "name", "image",
                    "description", "price", "location", "created", "user").filter(id=id))
    print(products)
    if not products:
        return JsonResponse({"error": "data not found"}, safe=False, status=404)
    images = list(ProductMultipleImage.objects.values(
        "images").filter(product=products[0]['id']))
    overviews = list(ProductOverview.objects.values(
        "name", "value").filter(product=products[0]['id']))
    imagesList = [getImageFullPath(products[0]['image'])]
    for image in images:
        imagesList.append(getImageFullPath(image['images']))
    products[0]['images'] = imagesList
    products[0]['overviews'] = overviews
    product = products[0]
    return JsonResponse(product, safe=False)


# define a fuction for key
def key_func(k):
    return k['category']


def getFeaturedList(request):
    products = list(Product.objects.values("id", "name", "image",
                    "price", "location", "category").filter(is_featured=True))
    if not products:
        return JsonResponse({"error": "data not found"}, safe=False, status=404)
    for index, product in enumerate(products):
        categories = list(Category.objects.values(
            "name").filter(id=product['category']))
        if categories:
            products[index]['category'] = categories[0]['name']
        else:
            products[index]['category'] = ""
    returnProducts = []
    for key, value in groupby(products, key_func):
        index = -1
        rents = []
        for val in list(value):
            val['image'] = getImageFullPath(val['image'])
            rents.append(val)

        for ind, pro in enumerate(returnProducts):
            if pro['category'] == key:
                index = ind
        if index == -1:
            returnProducts.append({"category": key, "rents": rents})
        else:
            returnProducts[index]['rents'].append(rents[0])
    print(returnProducts)
    return JsonResponse(returnProducts, safe=False)


def getSearchList(request, search_key):
    products = list(Product.objects.values("id", "name", "image",
                    "price", "location", "category").filter(Q(name__contains=search_key.lower()) | Q(location__contains=search_key.lower())))
    if not products:
        return JsonResponse({"error": "data not found"}, safe=False, status=404)
    for index, product in enumerate(products):
        products[index]['image'] = getImageFullPath(products[index]['image'])
        categories = list(Category.objects.values(
            "name").filter(id=product['category']))
        if categories:
            products[index]['category'] = categories[0]['name']
        else:
            products[index]['category'] = ""
    return JsonResponse(products, safe=False)


def getAllProductsWithCategoryName(request, category):
    products = list(Product.objects.values(
        "id", "name", "image", "price", "location", "category"))
    for index, product in enumerate(products):
        categories = list(Category.objects.values(
            "name").filter(id=product['category']))
        if categories:
            products[index]['category'] = categories[0]['name']
        else:
            products[index]['category'] = ""
    productsList = []
    for pro in products:
        if pro['category'] == category:
            pro['image'] = getImageFullPath(pro['image'])
            productsList.append(pro)
    if not productsList:
        return JsonResponse({"error": "data not found"}, safe=False, status=404)
    return JsonResponse(productsList, safe=False)


def getAllCategories(request):
    categories = list(Category.objects.values())
    if not categories:
        return JsonResponse({"error": "data not found"}, safe=False, status=404)
    catList = []
    for cat in categories:
        cat["image"] = getImageFullPath(cat['image'])
        catList.append(cat)
    return JsonResponse(catList, safe=False)
