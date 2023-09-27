from django.urls import path
from ProyectoWebApp import views
from django.conf import settings
from django.conf.urls.static import static #para las carpetas de las imagenes y creación de la subcarpeta

urlpatterns =[
    path('', views.home, name="Home"),
]
#añadimos la ruta para las imagenes
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)