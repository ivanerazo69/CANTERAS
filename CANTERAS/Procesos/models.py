from django.db import models

# Create your models here.
class Artificial_neural_networks(models.Model):
    Extracion = models.TextField()
    Municipio = models.TextField()
    Zona = models.TextField()
    Vereda = models.TextField()
    Nombre_Fuente = models.TextField()
    Observacion = models.TextField()
    Observacion_2 = models.TextField()
    Dureza  = models.FloatField(blank=True, null=True)
    IP = models.FloatField(blank=True, null=True)
    CBR = models.FloatField(blank=True, null=True)

    class Meta():
        verbose_name = 'red_neuronal'
        verbose_name_plural = 'redes_neuronales'
