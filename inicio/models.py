from django.db import models

# Modelo para la tabla 'lineas'
class Linea(models.Model):
    id_linea = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    no_estaciones = models.IntegerField(blank=True, null=True)
    id_municipalidades = models.ForeignKey('Municipalidad', models.DO_NOTHING, db_column='id_municipalidades', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'linea'  # <- ESTO ES CLAVE




# Modelo para la tabla 'estacion'
class Estacion(models.Model):
    id = models.AutoField(primary_key=True)
    linea_id = models.IntegerField()
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200)
    orden = models.IntegerField()

    class Meta:
        managed = False  # No crear ni modificar tabla
        db_table = 'estacion'
        ordering = ['orden']

    def __str__(self):
        return f"{self.orden}. {self.nombre}"

class Municipalidad(models.Model):
    id_municipalidad = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'municipalidad'
