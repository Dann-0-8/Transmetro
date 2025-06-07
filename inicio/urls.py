from django.urls import path
from .views import login_view, logout_view, dashboard, estaciones_por_linea
from .views import agregar_estacion
from .views import guardar_estado_estaciones
from .views import datos_administrativos
from .views import datos_administrativos


urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('linea/<int:linea_id>/', estaciones_por_linea, name='estaciones_por_linea'),
   path('linea/<int:linea_id>/agregar-estacion/', agregar_estacion, name='agregar_estacion'),
    path('linea/<int:linea_id>/guardar-estados/', guardar_estado_estaciones, name='guardar_estado_estaciones'),
    path('admin/datos/', datos_administrativos, name='datos_administrativos'),
     path('admin/datos/', datos_administrativos, name='datos_administrativos'),
]
