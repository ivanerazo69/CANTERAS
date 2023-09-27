from django.shortcuts import render, HttpResponse
from Dashboard.models import dasboard
from django.views.generic import TemplateView
from django.http.response import JsonResponse
import json
import tensorflow as ft
#from tensorflow.keras.models import load_model
import os
import os
import keras
import keras
from keras.models import load_model
from pathlib import Path
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

#/-----------------------REDES NEURONALES ARTIFICIALES---------------------------/
def predecir_fuente_extraccion(request):
    # Inicializar las variables
    resultado = None
    etiqueta = None
    fuentes_dict = []
    nombres_fuentes = []
    if request.method=='POST':
        # Obtener los valores del formulario
        dureza = request.POST.get('maquina')
        indice_plasticidad = request.POST.get('ip')
        cbr=request.POST.get('cbr')
        print("Valores obtenidos del formulario:")
        print("Dureza:", dureza)
        print("Indice de plasticidad:", indice_plasticidad)
        print("CBR:", cbr)

    # Verificar que los campos no sean None antes de convertirlos a float
        if dureza is not None and indice_plasticidad is not None and cbr is not None:
            dureza = float(dureza)
            indice_plasticidad = float(indice_plasticidad)
            cbr = float(cbr)

            # Cargar el modelo de red neuronal previamente entrenado
            ruta_modelo = Path(__file__).resolve().parent.parent / 'modelo_entrenado' / 'modelofinalf.keras'
            modelo = load_model(ruta_modelo)
            
            if modelo is None:
                # Manejar el caso en que el modelo no se cargó correctamente
                return {
                    'resultado_prediccion': None,
                    'etiqueta': "Error en carga del modelo",
                    'fuentes_cercanas': [],
                    'nombres_fuentes_cercanas': []
                }

            # Preparar los datos para la predicción
            datos_prediccion = [[dureza, indice_plasticidad, cbr]]
            datos_prediccion = np.array(datos_prediccion)
            
            # Hacer la predicción
            prediccion = modelo.predict(datos_prediccion)            

            # La predicción es un arreglo de un solo elemento, obtener el valor de la predicción
            resultado = prediccion[0][0]
            probabilidad = prediccion[0][0]

            # Establecer el umbral de probabilidad (0.0025 en este caso)
            umbral = 0.6

            # Asignar etiqueta de clasificación binaria
            if probabilidad < umbral:
                etiqueta = "cumple requisitos"
            else:
                etiqueta = "no cumple requisitos"

            # Obtener las fuentes de extracción que cumplen con los requisitos de entrenamiento
            fuentes_cumplen_requisitos = dasboard.objects.filter(Dureza_maquina_angeles__lte=50,
                                                                IP__lte=9,
                                                                CBR__gte=15)
            # Puedes convertir las fuentes obtenidas en un diccionario si lo deseas
            fuentes_dict = [{'Dureza_maquina_angeles': fuente.Dureza_maquina_angeles,
                             'IP': fuente.IP,
                             'CBR': fuente.CBR} for fuente in fuentes_cumplen_requisitos]
            # Obtener los nombres de las fuentes cercanas
            nombres_fuentes = [fuente.nombre_fuente for fuente in fuentes_cumplen_requisitos]

            # Retornar los valores como un diccionario
            return {'resultado_prediccion': resultado,
                    'etiqueta':etiqueta, 
                    'fuentes_cercanas': fuentes_dict,
                    'nombres_fuentes_cercanas': nombres_fuentes,}
        else:
            # Manejar el caso en que los valores del formulario no son válidos
            return {
                'resultado_prediccion': None,
                'etiqueta': "Valores del formulario no válidos",
                'fuentes_cercanas': [],
                'nombres_fuentes_cercanas': []
            }
    else:
        # Retornar un diccionario con valores predeterminados o un mensaje de error
        return {
            'resultado_prediccion': None,
            'etiqueta': "No se enviaron datos del formulario",
            'fuentes_cercanas': [],
            'nombres_fuentes_cercanas': [],
        }
#/------------------------------------------------------------------------/        

# vista para el formulario
def procesos(request):
    print("Llamando a la función predecir_fuente_extraccion")
    #método 'value_list('parametro', flat=True)=devuelve un objeto QuerySet que contiene los valores de una sola columna, en este caso el valor del atributo "zona" del modelo "dasboard", es decir: ['Norte', 'Centro', 'Sur', 'Oriente']
    #el argumento "flat=True" en Django se utiliza en una consulta a la base de datos para obtener una lista plana de valores en lugar de una lista de diccionarios o una lista de tuplas.
    #la función .distinct() se utiliza en una consulta a la base de datos para obtener valores únicos de un campo en particular. Se aplica a un QuerySet y devuelve un nuevo QuerySet que contiene los objetos únicos en función de los campos espeficiados en la llamada a 'distinct()'.  Por ejemplo, si tenemos un modelo Product con un campo category y queremos obtener una lista de todas las categorías únicas en nuestra base de datos, podemos hacer lo siguiente: unique_categories = Product.objects.values('category').distinct(), Esto devolverá un QuerySet que contiene una sola instancia de cada categoría única en la base de datos. La función distinct() se utiliza en combinación con la función values() para especificar el campo del modelo que se utilizará para determinar la unicidad de los objetos en la consulta.
    #zonas=list(dasboard.objects.values_list('zona', flat=True).distinct())
    #municipios=list(dasboard.objects.values_list('municipio', flat=True).distinct())
    #/-----------------------FILTROS---------------------------/
    municipios=list(dasboard.objects.values_list('municipio', flat=True).distinct())
    norte=list(dasboard.objects.filter(zona='Norte').values_list('municipio', flat=True).distinct())
    sur=list(dasboard.objects.filter(zona='Sur').values_list('municipio', flat=True).distinct())
    centro=list(dasboard.objects.filter(zona='Centro').values_list('municipio', flat=True).distinct())
    oriente=list(dasboard.objects.filter(zona='Oriente').values_list('municipio', flat=True).distinct())

    municipios_json=json.dumps(municipios)
    norte_json=json.dumps(norte)
    sur_json=json.dumps(sur)
    centro_json=json.dumps(centro)
    oriente_json=json.dumps(oriente)
    #/---------------------REDES NEURONALES-------------------/
    valores_prediccion = predecir_fuente_extraccion(request)

    # Obtener la etiqueta de clasificación binaria
    etiqueta = valores_prediccion['etiqueta']
    # Obtener los nombres de las fuentes cercanas
    nombres_fuentes_cercanas = valores_prediccion['nombres_fuentes_cercanas']
    #Obtener los ensayos de las fuentes cercanas que cumplen según los datos del formulario
    ensayos_fuentes_prediccion=valores_prediccion['fuentes_cercanas']
    #Obtenemos la probabilidad que arroja la predicción: 1>cumple 0<no cumple
    probabilidad=valores_prediccion['resultado_prediccion']
    #/-----------------------CONTEXTO---------------------------/
    contexto={
        'municipios':municipios_json,
        'norte':norte_json,
        'sur':sur_json,
        'centro':centro_json,
        'oriente':oriente_json,
        'etiqueta_prediccion': etiqueta,  # Pasar la etiqueta al contexto
        'nombres_fuentes_cercanas': nombres_fuentes_cercanas,  # Pasar los nombres al contexto
        'ensayos_fuentes_prediccion':ensayos_fuentes_prediccion, #Pasar los ensayos de las fuentes de predicción
        'probabilidad':probabilidad, #pasamos la probabilidad para obtenerla en el template
    }
    return render(request, 'Procesos/procesos.html', contexto) 