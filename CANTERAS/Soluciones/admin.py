from django.contrib import admin
from Soluciones.models import franjas
from Soluciones.models import grafo
# Register your models here.

class franjasAdmin(admin.ModelAdmin):
    list_display=('tamiz','MSA38','MIA38','MSA25','MIA25','TamboMa','TamboCh','MoralesSB','MoralesSC','TotoroSab','TotoroSA','RosasTr','RosasUf','BolivarSR','BolivarCol','Piendamo','PopayanBe','PopayanCer','LaSierra','SotaraHB','SotaraSR','CaldonoEs','CaldonoJa','VillaRicaBP','VillaRicaSB','Guachene','LaVegaCR','LaVegaUv')
    search_fields=('tamiz',)
    list_filter=('tamiz',)

class grafoAdmin(admin.ModelAdmin):
    list_display=('NODO','CONEXION','DISTANCIA')
    search_fields=('NODO',)
    list_filter=('NODO',)

admin.site.register(franjas, franjasAdmin)
admin.site.register(grafo, grafoAdmin)

