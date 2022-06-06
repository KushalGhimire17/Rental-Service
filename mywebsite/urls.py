
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
