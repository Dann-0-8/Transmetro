from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .models import Linea, LineaEstacion, Estacion


def bienvenida(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        user = authenticate(username=usuario, password=password)

        if user:
            return redirect('dashboard')
        else:
            return render(request, 'bienvenida.html', {'mensaje': 'Credenciales incorrectas'})

    return render(request, 'bienvenida.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def ver_linea(request, id_linea):
    try:
        linea = Linea.objects.get(id_linea=id_linea)
        estaciones = Estacion.objects.filter(lineaestacion__id_linea=linea).order_by('lineaestacion__orden')
        return render(request, 'linea.html', {'linea': linea, 'estaciones': estaciones})
    except Linea.DoesNotExist:
        return redirect('dashboard')
