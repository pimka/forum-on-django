from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserCredentialsModel, UserToken


admin.site.register([UserCredentialsModel, UserToken])
