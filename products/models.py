from django.db import models
from taggit.managers import TaggableManager
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    # status choice field : available, pending, booked
    user = models.ForeignKey("accounts.User", related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images', null=True, blank=True)
    price = models.FloatField(default=0)
    location = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_posted = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    tags = TaggableManager()

    def get_tags(self):
        return self.tags.names()

    def __str__(self):
        return f'Product: {self.name} - Posted by: {self.user.phone}'

class ProductMultipleImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'Image of {self.product.name}'


class BookProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    profile = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Product: {self.product.name} / Booked by {self.profile.user.phone}'


class Message(models.Model):
    """A model to pass message in a contact us page"""
    email = models.EmailField()
    phone = models.IntegerField()
    message = models.TextField(help_text="Enter your message here")


class Company(models.Model):
    """A model to take company details """
    email = models.EmailField()
    phone = models.IntegerField()
    location = models.CharField(max_length=256)



class ProductOverview(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    
class FeaturedProduct(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, unique=True)