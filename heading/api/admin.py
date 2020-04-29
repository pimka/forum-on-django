from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import HeadingModel, TagModel

admin.site.register([HeadingModel, TagModel])