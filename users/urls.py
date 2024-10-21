from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, ProfileView, CustomPasswordReset, UserListView, \
    UserDetailView, UserDeleteView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("users/<int:pk>/update", UserUpdateView.as_view(), name="user_update"),
    path("users/<int:pk>/delete", UserDeleteView.as_view(), name="user_delete"),
    path('password_reset/', CustomPasswordReset.as_view(), name='password_reset')

]
