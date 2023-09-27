from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, HttpRequest


# Create your views here.
def home(request):
    return render(request, 'ProyectoWebApp/home.html')


