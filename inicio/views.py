from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Linea, Estacion
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'bienvenida.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'bienvenida.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    lineas = Linea.objects.all()

    colores_por_linea = {
        1: "#6f2da8",     # Morado
        2: "#9c27b0",     # Morado claro
        6: "#ffc107",     # Amarillo
        7: "#6c757d",     # Gris
        12: "#ff5722",    # Naranja
        13: "#4caf50",    # Verde
        18: "#03a9f4",    # Celeste
    }

    for linea in lineas:
        linea.color = colores_por_linea.get(linea.id_linea, "#6c757d")

    return render(request, 'dashboard.html', {'lineas': lineas})


@login_required
def estaciones_por_linea(request, linea_id):
    colores_por_linea = {
        1: "#6f2da8",     # Morado
        2: "#9c27b0",     # Morado claro
        6: "#ffc107",     # Amarillo
        7: "#6c757d",     # Gris
        12: "#ff5722",    # Naranja
        13: "#4caf50",    # Verde
        18: "#03a9f4",    # Celeste
    }

    try:
        linea = Linea.objects.get(id_linea=linea_id)
        linea.color = colores_por_linea.get(linea.id_linea, "#6c757d")
    except Linea.DoesNotExist:
        linea = None

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT e.id_estacion, e.nombre, e.activa
            FROM linea_estacion le
            JOIN estacion e ON le.id_estacion = e.id_estacion
            WHERE le.id_linea = %s
            ORDER BY le.orden
        """, [linea_id])
        estaciones = []
        for row in cursor.fetchall():
            estaciones.append({
                'id_estacion': row[0],
                'nombre': row[1],
                'activa': row[2],
                'direccion': ''
            })

    return render(request, 'linea.html', {'linea': linea, 'estaciones': estaciones})


@csrf_exempt
@login_required
def agregar_estacion(request, linea_id):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        orden = int(request.POST.get('orden'))

        with connection.cursor() as cursor:
            cursor.execute("SELECT IFNULL(MAX(id_estacion), 0) + 1 FROM estacion")
            nueva_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO estacion (id_estacion, nombre) VALUES (%s, %s)", [nueva_id, nombre])

            cursor.execute("""
                INSERT INTO linea_estacion (id_linea, id_estacion, orden)
                VALUES (%s, %s, %s)
            """, [linea_id, nueva_id, orden])

        return HttpResponseRedirect(reverse('estaciones_por_linea', args=[linea_id]))

@csrf_exempt
@login_required
def guardar_estado_estaciones(request, linea_id):
    if request.method == 'POST':
        estados = request.POST

        with connection.cursor() as cursor:
            for key in estados:
                if key.startswith('estacion_'):
                    estacion_id = int(key.replace('estacion_', ''))
                    activa = 1 if estados[key] == 'on' else 0
                    cursor.execute(
                        "UPDATE estacion SET activa = %s WHERE id_estacion = %s",
                        [activa, estacion_id]
                    )

        return HttpResponseRedirect(reverse('estaciones_por_linea', args=[linea_id]))

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render

@login_required
def datos_administrativos(request):
    tablas = ['linea', 'estacion', 'bus', 'parqueo', 'guardia', 'operador', 'piloto', 'pc_estacion', 'acceso', 'municipalidad']
    datos = {}
    resultados = None
    error = None
    consulta = ''

    if request.method == 'POST':
        consulta = request.POST.get('consulta_sql', '').strip()
        try:
            if consulta.lower().startswith('select'):
                with connection.cursor() as cursor:
                    cursor.execute(consulta)
                    columnas = [col[0] for col in cursor.description] if cursor.description else []
                    filas = cursor.fetchall() if columnas else []
                    resultados = {
                        'columnas': columnas,
                        'filas': filas
                    }
            else:
                error = "Solo se permiten consultas SELECT."
        except Exception as e:
            error = str(e)

    # Mostrar las tablas predeterminadas
    with connection.cursor() as cursor:
        for tabla in tablas:
            try:
                cursor.execute(f"SELECT * FROM {tabla} LIMIT 100")
                columnas = [col[0] for col in cursor.description]
                filas = cursor.fetchall()
                datos[tabla] = {
                    'columnas': columnas,
                    'filas': filas
                }
            except:
                pass  # Ignorar errores en tablas inexistentes o sin permisos

    return render(request, 'datos_admin.html', {
        'datos': datos,
        'resultados': resultados,
        'error': error,
        'consulta': consulta
    })
