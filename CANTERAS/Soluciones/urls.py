from django.urls import path
from Soluciones import views

urlpatterns =[
    path('', views.soluciones, name='Soluciones'),
    path('mostrar_grafo/', views.mostrar_grafo, name='mostrar_grafo'),
]