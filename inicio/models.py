from django.db import models

class Municipalidad(models.Model):
    id_municipalidad = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'municipalidad'


class Estacion(models.Model):
    id_estacion = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    cantidad_accesos = models.IntegerField(blank=True, null=True)
    id_municipalidades = models.ForeignKey(Municipalidad, models.DO_NOTHING, db_column='id_municipalidades', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estacion'


class Linea(models.Model):
    id_linea = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    no_estaciones = models.IntegerField(blank=True, null=True)
    id_municipalidades = models.ForeignKey(Municipalidad, models.DO_NOTHING, db_column='id_municipalidades', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'linea'


class LineaEstacion(models.Model):
    id_linea = models.ForeignKey(Linea, models.DO_NOTHING, db_column='id_linea')
    id_estacion = models.ForeignKey(Estacion, models.DO_NOTHING, db_column='id_estacion')
    orden = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'linea_estacion'
