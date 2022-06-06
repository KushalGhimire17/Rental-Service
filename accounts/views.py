from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import generics

from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer, ProfileSerializer
from .models import Profile, User

from .permissions import IsUserOrAdmin

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrAdmin]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    lookup_field = 'id'


class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        errors = []

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            try:
                validate_password(password=serializer.data.get("new_password"))
            except ValidationError as error:
                errors.append(error)
                return Response(error ,status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileListView(generics.ListCreateAPIView):
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication, SessionAuthentication]