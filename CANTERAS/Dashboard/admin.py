from django.contrib import admin
from Dashboard.models import dasboard, produccion
# Register your models here.

class dasboardAdmin(admin.ModelAdmin):
    list_display=('municipio','zona','tipoextraccion','observacion_fuente','Dureza_maquina_angeles','Requisito_Dureza_NT1','LL_Maximo','LL_Requisito','IP','Requisito_IP','CBR','CBR_Requisito')
    search_fields=('tipoextraccion',)
    list_filter=('municipio','tipoextraccion')
    date_hierarchy='fecha'

class produccionAdmin(admin.ModelAdmin):
    list_display=('MUNICIPIO','CAFE','CAÑA','PINO_Y_EUCALIPTO','FIQUE')
    search_fields=('MUNICIPIO',)
    list_filter=('MUNICIPIO',)

admin.site.register(dasboard, dasboardAdmin)
admin.site.register(produccion, produccionAdmin)