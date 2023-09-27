from django.db import models

# Create your models here.
class Fuente_Inicial(models.Model):
    pr= models.TextField(blank=True, null=True)
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
    imagen=models.ImageField(blank=True, null=True, upload_to='busquedas') #subcarpeta ='busquedas'
    Distancia_Cabecera=models.FloatField(blank=True, null=True)
    Tiempo_Viaje_Cabecera=models.FloatField(blank=True, null=True)
    ESTUDIO_S_N=models.CharField(max_length=5)
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
        verbose_name='busqueda'
        verbose_name_plural='busquedas'
    def __str__(self):
        return self.nombre_fuente