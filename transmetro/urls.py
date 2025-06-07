from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('', include('inicio.urls')),  # Esto es obligatorio
    path('admin/', admin.site.urls),
]
