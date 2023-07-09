from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('auth.urls')),
    path('api/', include('user.urls')),
    path('api/', include('lesson.urls'))
]
