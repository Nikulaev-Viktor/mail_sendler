from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordResetForm
from django import forms
from sendler.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'phone_number', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserModeratorForm(StyleFormMixin, UserChangeForm):
    """Форма модератора для редактирования профиля пользователя"""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class ResetPasswordForm(StyleFormMixin, PasswordResetForm):
    class Meta:
        model = User
        fields = ('email',)

