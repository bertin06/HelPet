from django.urls import path
from .views import ChatList, Chat

urlpatterns = [
    path('', ChatList.as_view(), name = 'chat-list'),
    path('<int:room>', Chat.as_view(), name = 'chat'),
]