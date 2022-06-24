from dataclasses import fields
from rest_framework import serializers
from .models import BookProduct, Message, Product, ProductMultipleImage, Category, Company

from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)



#==========================================
"""
Change Json to string in tag input
"""
import six

class NewTagListSerializerField(TagListSerializerField):
    def to_internal_value(self, value):
        if isinstance(value, six.string_types):
            value = value.split(',')

        if not isinstance(value, list):
            self.fail('not_a_list', input_type=type(value).__name__)

        for s in value:
            if not isinstance(s, six.string_types):
                self.fail('not_a_str')

            self.child.run_validation(s)
        return value

#===========================================


#==============================================
"""
Serialize the product model
"""
class ProductSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = NewTagListSerializerField()
    

    class Meta:
        model = Product
        fields = ['id', 'user', 'name', 'description', 'image', 'price', 'location', 'created', 'updated', 'category', 'tags']
        read_only_fields = ("user", "is_posted", "is_featured")
    
#===========================================


#==============================================
"""
Serialize the productmultipleimage model
"""

class ProductMultipleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMultipleImage
        fields = '__all__'

#===========================================


#==============================================
"""
Serialize the category model
"""

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

#==============================================


#===========================================
"""
Serialize the book product model
"""
class BookProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookProduct
        fields = '__all__'

#==============================================

class MessageSerializer(serializers.ModelSerializer):
    """Message serializer to accept message from contact us page"""
    class Meta:
        model = Message
        fields = '__all__'



#==============================================

class CompanySerializer(serializers.ModelSerializer):
    """Company serializer to accept company details """
    class Meta:
        model = Company
        fields = '__all__'

class ProductMultipleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMultipleImage
        fields = '__all__'