from django.urls import path
from Procesos import views

urlpatterns =[
    path('', views.procesos, name='Procesos'),
    path('', views.predecir_fuente_extraccion, name='predecir_fuentes'),
]