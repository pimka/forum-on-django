"""gateway URL Configuration

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
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
import api.views.open as open
import api.views.close as close

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_headings/', open.GetHeadingsView.as_view()),
    path('get_heading/', open.GetConcreteHeadingView.as_view()),
    path('get_tags/', open.GetTagsView.as_view()),
    path('get_messages/', open.GetMessagesView.as_view()),
    path('get_message/', open.GetConcreteMessageView.as_view()),
    path('add_user/', open.UsersView.as_view()),
    path('get_user/', open.GetConcreteUserView.as_view()),
    path('heading/<uuid:head_uuid>/get_messages/', open.GetHeadingMessagesView.as_view()),
    
    path('refresh/', close.RefreshTokenView.as_view()),
    path('revoke/', close.RevokeTokenView.as_view()),
    path('code-exchange/', open.CodeExchangeView.as_view()),
    
    path('heading/', close.PostHeadingsView.as_view()),
    path('heading/<uuid:head_uuid>/', close.ConcreteHeadingView.as_view()),
    path('tags/', close.TagsView.as_view()),
    path('tag/<uuid:tag_uuid>/', close.ConcreteTagView.as_view()),
    path('messages/', close.MessagesView.as_view()),
    path('message/<uuid:mes_uuid>/', close.ConcreteMessageView.as_view()),
    path('user/<uuid:user_uuid>/', close.ConcreteUserView.as_view()),
    path('heading/<uuid:head_uuid>/messages/', close.HeadingMessagesView.as_view()),
    path('heading/<uuid:head_uuid>/message/<uuid:mes_uuid>/', close.ConcreteHeadingMessageView.as_view())
]
