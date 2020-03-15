from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from api.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'is_moderate', )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'is_moderate', )