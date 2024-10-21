from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordResetForm
from django import forms
from django.forms import ModelForm

from sendler.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форм для регистрации пользователя"""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """Форма для авторизации пользователя"""
    class Meta:
        model = User
        fields = ('email', 'password')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """Форма для редактирования профиля пользователя"""
    class Meta:
        model = User
        fields = ('first_name', 'email', 'phone_number', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserForm(StyleFormMixin, ModelForm):
    """Форма для блокировки пользователя"""
    class Meta:
        model = User
        fields = ("is_active",)


class ResetPasswordForm(StyleFormMixin, PasswordResetForm):
    """Форма для сброса пароля"""
    class Meta:
        model = User
        fields = ('email',)
