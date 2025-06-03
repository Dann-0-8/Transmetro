from django.urls import path
from . import views

urlpatterns = [
    path('', views.bienvenida, name='bienvenida'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('linea/<int:id_linea>/', views.ver_linea, name='ver_linea'),
]
