from django.db import models

# Create your models here.
class dasboard(models.Model):
    tipoextraccion=models.CharField(max_length=150)
    nombre_fuente=models.TextField()
    observacion_fuente=models.TextField()
    otras_observaciones=models.TextField()
    codigo=models.TextField()
    fecha=models.DateField(blank=True, null=True)
    coordenada_Latitud=models.FloatField()
    coordenada_Longitud=models.FloatField()
    municipio=models.CharField(max_length=150)
    vereda=models.CharField(max_length=255, null=False, default='Agrega el nombre del lugar donde se tomá el punto')
    zona=models.CharField(max_length=10)
    Distancia_Cabecera=models.FloatField(blank=True, null=True)
    Tiempo_Viaje_Cabecera=models.FloatField(blank=True, null=True)
    Dureza_maquina_angeles=models.FloatField(blank=True, null=True)
    Requisito_Dureza_NT1=models.FloatField(blank=True, null=True)
    LL_Maximo=models.FloatField(blank=True, null=True)
    LL_Requisito=models.FloatField(blank=True, null=True)
    IP=models.FloatField(blank=True, null=True)
    Requisito_IP=models.CharField(max_length=20)	
    CBR=models.FloatField(blank=True, null=True)
    CBR_Requisito=models.FloatField(blank=True, null=True)
    Relacion_P200_P10=models.FloatField(blank=True, null=True)
    Requisito_Relacion_P200_P10=models.CharField(max_length=20)
    Relacion_P200_P40=models.FloatField(blank=True, null=True)
    Requisito_Relacion_P200_P40=models.FloatField(blank=True, null=True)
    Relacion_Resultado=models.FloatField(blank=True, null=True)
    Requisito_Relacion_Resultado=models.CharField(max_length=20)
    Angularidad_Finos_sin_compactar=models.FloatField(blank=True, null=True)
    Clasificacion_SUCS=models.TextField()
    Gravedad_Especifica=models.FloatField(blank=True, null=True)
    Masa_Unitaria_Suelta=models.FloatField(blank=True, null=True)
    Masa_Unitaria_Compacta=models.FloatField(blank=True, null=True)
    Absorcion_agregado_fino=models.FloatField(blank=True, null=True)
    Absorcion_agregado_grueso=models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name='dasboard'
        verbose_name_plural='dasboards'
    def __str__(self):
        return self.nombre_fuente

class produccion(models.Model):
    MUNICIPIO=models.CharField(max_length=30)	
    DEPARTAMENTO=models.CharField(max_length=30)
    LATITUD=models.FloatField(blank=True, null=True)
    LONGITUD=models.FloatField(blank=True, null=True)
    CAFE=models.FloatField(blank=True, null=True)
    FAMILIAS_CAFE=models.FloatField(blank=True, null=True)
    CAÑA=models.FloatField(blank=True, null=True)
    FAMILIAS_CAÑA=models.FloatField(blank=True, null=True)
    PINO_Y_EUCALIPTO=models.FloatField(blank=True, null=True)
    FIQUE=models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name='produccion'
        verbose_name_plural='producciones'
    
    def __str__(self):
        return self.MUNICIPIO