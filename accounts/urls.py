from django.urls import path
from .views import UserDetail, UserList, UserRegister, ChangePasswordView, ProfileView, ProfileListView


urlpatterns = [
    path('',UserList.as_view() ,name='user-list'),
    path('<int:id>/',UserDetail.as_view() ,name='user-detail'),
    path('register/',UserRegister.as_view() ,name='user-create'),
    path('change-password/',ChangePasswordView.as_view() ,name='change-password'),
    path('profiles/',ProfileListView.as_view() ,name='profile-list'),
    path('profiles/<int:id>/',ProfileView.as_view() ,name='profile'),
]