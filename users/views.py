import secrets
import random
import string

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from users.forms import UserRegisterForm, UserLoginForm, UserProfileForm
from users.models import User
from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    """Контроллер создания пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class CustomPasswordReset(PasswordResetView):
    """Контроллер сброса пароля"""

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = get_object_or_404(User, email=email)
        characters = string.ascii_letters + string.digits + string.punctuation
        new_password = ''.join(random.choice(characters) for _ in range(12))
        user.password = make_password(new_password)
        send_mail(
            subject='Вы сменили пароль',
            message=f'Ваш новый пароль {new_password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        user.save()

        return super().form_valid(form)


class UserLoginView(LoginView):
    """Контроллер логина"""
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True


class ProfileView(LoginRequiredMixin, UpdateView):
    """Контроллер профиля"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, ListView):
    """Контроллер списка пользователей"""
    model = User
    template_name = 'user_list.html'
    # permission_required = 'users.can_view_user'


class UserDetailView(LoginRequiredMixin, DetailView):
    """Контроллер пользователя"""
    model = User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования пользователя"""
    model = User
    fields = [
        'id',
        'email',
        'is_active',
    ]
    success_url = reverse_lazy('users:user_list')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:user_list')
