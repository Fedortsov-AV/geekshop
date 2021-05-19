from django import forms

from authapp.forms import UserRegisterForm
from authapp.models import User


class UserAdminRegisterForm(UserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'image', 'email', 'first_name', 'last_name', 'password1', 'password2')


