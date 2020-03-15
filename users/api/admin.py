from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from api.forms import CustomUserChangeForm, CustomUserCreationForm
from api.models import User

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'uuid', 'is_moderate']

admin.site.register(User, CustomUserAdmin)