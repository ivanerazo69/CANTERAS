from django.urls import path
from Dashboard import views

urlpatterns =[
    path('', views.dashboard, name='Dashboard'),
]
