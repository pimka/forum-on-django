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

# http://localhost:8080/oauth2/authorize?response_type=code&state=random_state_string&client_id=x6kmOcoE9Ft3peTuXiALmNfyCf7Y62UaF8NBHNc5
urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth2/logged-in/', OAuth2View.as_view()),
    path('tokens/', ServicesTokenView.as_view(), name='tokens'),
    path('user/auth/', AuthTokenView.as_view(), name='auth'),
    path('user/add/', UsersBaseView.as_view()),
    path('user/login/', UsersLoginView.as_view(), name='login_user'),
    path('user/<uuid:uuid>/', UsersAdvancedView.as_view()),

    path("oauth2/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns = format_suffix_patterns(urlpatterns)
