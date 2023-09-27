from django.urls import path
from Busqueda import views

urlpatterns =[
    path('', views.busqueda, name='Busqueda'),
    path('graficos/', views.grafica_fuentes, name='graficos'),
    path('mapa/', views.mapa, name='mapa'),
    path('buscar-municipio/', views.buscarMun, name='buscar_municipio'),
    path('procesos/', views.procesos, name='procesos'),
    path('busquedaFuente/', views.busquedaFuente, name='Busqueda_Fuente'),
]