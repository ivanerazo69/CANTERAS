from django.contrib import admin
from Busqueda.models import Fuente_Inicial
# Register your models here.

class fuenteAdmin(admin.ModelAdmin):
    # Permitir visualizar los atributos del modelo
    list_display=('tipoextraccion', 'nombre_fuente', 'observacion_fuente','coordenada_Latitud','coordenada_Longitud','municipio','zona','vereda','ESTUDIO_S_N')
    #realizar busquedas:
    search_fields=('municipio','fecha','tipoextraccion')
    #permitir filtrar por un atributo del modelo
    list_filter=('municipio','tipoextraccion',)
    #permitir un selector de fechas:
    date_hierarchy='fecha'
admin.site.register(Fuente_Inicial, fuenteAdmin)