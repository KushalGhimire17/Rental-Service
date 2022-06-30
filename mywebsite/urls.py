from django.contrib import admin
from django.urls import path, include

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

from products.views import MessageList, MessageDetail, CompanyList, CompanyDetail

from products import views

API_TITLE = 'Rent API'
API_DESCRIPTION = 'A web api for CRUD operations along with permissions mixins'
schema_view = get_schema_view(title=API_TITLE)
schema_view_swagger = get_swagger_view(title=API_TITLE)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('api-auth/', include('rest_framework.urls')),

    path('message/', MessageList.as_view(), name='message-list'),
    path('message/<int:pk>/', MessageDetail.as_view(), name='message-detail'),

    path('company/', CompanyList.as_view(), name='company-list'),
    path('company/<int:pk>/', CompanyDetail.as_view(), name='company-detail'),

    path('schema/', schema_view),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path('swagger-docs/', schema_view_swagger),


    path('api/categories/',
         views.getAllCategories, name="Categories Detail"),

    path('api/product/detail/<int:id>/',
         views.getProductDetail, name="Product Detail"),
    path('api/product/featured/',  views.getFeaturedList, name="Featured Products"),

    path('api/search/<str:search_key>/',
         views.getSearchList, name="Search Result"),
    path('api/all/<str:category>/',
         views.getAllProductsWithCategoryName, name="Products")
]
