from rest_framework import serializers
from .models import User, Profile
from django.contrib.auth import password_validation
from products.models import BookProduct
from django.http import JsonResponse

#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ['password']
    read_only_fields = ['last_login', 'date_joined', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions']


class RegisterSerializer(serializers.ModelSerializer):
   
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('phone', 'password', 'password2',)
        extra_kwargs = {
            'password': {
                'style': {'input_type': 'password'}
            }
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            phone=validated_data['phone'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value


class ProfileSerializer(serializers.ModelSerializer):
    booked_items = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ['id','avatar','user','booked_items']

    def get_booked_items(self, obj):
        items = None
        print(obj)
        user = self.context['request'].user
        print("user", user)
        print("id", user.id)
        if obj:
            # items = BookProduct.objects.filter(profile__user=obj.user)
            items = BookProduct.objects.all().values_list()
            res = {
                'items': list(items),
            }
            for item in items:
                print("item is ",item)
        return JsonResponse(res)