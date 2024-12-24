from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('', include('base.urls')),
    path('chat/', include('chat.urls')),
    path('register/', include('register.urls')),
]
