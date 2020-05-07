"""auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import (AuthTokenView, OAuth2View, ServicesTokenView,
                       UsersAdvancedView, UsersBaseView, UsersLoginView)

# http://127.0.0.1:8080/accounts/login/?next=/oauth2/authorize/%3Fclient_id%3DxM3AOMPLsDxC0AeFU6nncrTOb4JJLxvIlUl1lwCj%26response_type%3Dcode%26state%3Drandom_state_string
urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth2/logged-in/', OAuth2View.as_view()),
    path('tokens/', ServicesTokenView.as_view()),
    path('user/auth/', AuthTokenView.as_view()),
    path('user/add/', UsersBaseView.as_view()),
    path('user/login/', UsersLoginView.as_view()),
    path('user/<uuid:uuid>/', UsersAdvancedView.as_view()),

    path("oauth2/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns = format_suffix_patterns(urlpatterns)
