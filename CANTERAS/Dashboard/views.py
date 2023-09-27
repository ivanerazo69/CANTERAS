from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, View, DetailView
from Dashboard.models import dasboard, produccion
from django.db.models import Sum
import pandas as pd
import json
from django.http.response import JsonResponse
import math
import geojson

#---------------------------------------//---------------------------------------
# Creamos la vista que tendrá todos los atributos del modelo.
def dashboard(request):
    #resumen
    datos1=dasboard.objects.filter(tipoextraccion='Cantera').count()
    cantera="{:,.0f}".format(datos1)
    datos2=dasboard.objects.filter(tipoextraccion='Rio').count()
    rio="{:,.0f}".format(datos2)
    datos3=dasboard.objects.filter(tipoextraccion='Acopio').count()
    acopio="{:,.0f}".format(datos3)
    #----------------------TABLAS DE PRODUCCIÓN Y ENSAYOS---------------------------
    producciones=produccion.objects.all()
    resultados=dasboard.objects.all()
    #------//-----------------GRÁFICAS----------------------------------------------
    #1.Filtros para CBR('values es un método de consula para especificar que campos de la base de datos se deben incluir)
    #Filtros para rio, cantera y acopio
    cbr=dasboard.objects.all().values('municipio','vereda', 'CBR')
    cbr_rio=dasboard.objects.filter(tipoextraccion='Rio').values('municipio','vereda', 'CBR')
    cbr_cantera=dasboard.objects.filter(tipoextraccion='Cantera').values('municipio','vereda', 'CBR')
    cbr_acopio=dasboard.objects.filter(tipoextraccion='Acopio').values('municipio','vereda', 'CBR')
    #Filtros para zona: Norte, Sur, Oriente y Centro
    cbr_norte=dasboard.objects.filter(zona='Norte').values('municipio', 'vereda', 'CBR')
    cbr_sur=dasboard.objects.filter(zona='Sur').values('municipio', 'vereda', 'CBR')
    cbr_oriente=dasboard.objects.filter(zona='Oriente').values('municipio', 'vereda', 'CBR')
    cbr_centro=dasboard.objects.filter(zona='Centro').values('municipio', 'vereda', 'CBR')
    # arrays para gráficar el cbr con sus filtros 'Rio', 'Cantera', 'Acopio'
    #completo cbr
    array_objetos_cbr = []
    for dato in cbr:
        x = f"{dato['municipio']}-{dato['vereda']}"
        y = dato['CBR']
        objeto = {"x": x, "y": y}
        array_objetos_cbr.append(objeto)
    #1.Rio
    array_objetos_cbr_rio = []
    for dato in cbr_rio:
        x = f"{dato['municipio']}-{dato['vereda']}"
        y = dato['CBR']
        objeto = {"x": x, "y": y}
        array_objetos_cbr_rio.append(objeto)
    #2.Cantera
    array_objetos_cantera = []
    for dato in cbr_cantera:
        x = f"{dato['municipio']}-{dato['vereda']}"
        y = dato['CBR']
        objeto = {"x": x, "y": y}
        array_objetos_cantera.append(objeto)
    #3.Acopio
    array_objetos_acopio = []
    for dato in cbr_acopio:
        x = f"{dato['municipio']}-{dato['vereda']}"
        y = dato['CBR']
        objeto = {"x": x, "y": y}
        array_objetos_acopio.append(objeto)

    #4.Norte
    array_objetos_norte=[]
    for dato in cbr_norte:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['CBR']
        objeto={"x":x, "y":y}
        array_objetos_norte.append(objeto)   
    #5.Sur
    array_objetos_sur=[]
    for dato in cbr_sur:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['CBR']
        objeto={"x":x, "y":y}
        array_objetos_sur.append(objeto)  
    #6.Oriente
    array_objetos_oriente=[]
    for dato in cbr_oriente:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['CBR']
        objeto={"x":x, "y":y}
        array_objetos_oriente.append(objeto)  
    #7.Centro
    array_objetos_centro=[]
    for dato in cbr_centro:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['CBR']
        objeto={"x":x, "y":y}
        array_objetos_centro.append(objeto)

    #Convertimos a Json
    grafica1=(json.dumps(array_objetos_cbr))
    grafica1_cbr_rio=(json.dumps(array_objetos_cbr_rio))
    grafica1_cbr_cantera=(json.dumps(array_objetos_cantera))
    grafica1_cbr_acopio=(json.dumps(array_objetos_acopio))
    grafica1_cbr_norte=(json.dumps(array_objetos_norte))
    grafica1_cbr_sur=(json.dumps(array_objetos_sur))
    grafica1_cbr_oriente=(json.dumps(array_objetos_oriente))
    grafica1_cbr_centro=(json.dumps(array_objetos_centro))
    #-----------------//-------------------
    #1.Filtros para LL
    #valores vacios para las tablas de ll
    #ll_cleaned = [x for x in ll if not math.isnan(x['LL_Maximo'])]
    ll=dasboard.objects.all().values('municipio','vereda', 'LL_Maximo')
    ll_rio=dasboard.objects.filter(tipoextraccion='Rio').values('municipio', 'vereda', 'LL_Maximo')
    ll_cantera=dasboard.objects.filter(tipoextraccion='Cantera').values('municipio', 'vereda', 'LL_Maximo')
    ll_acopio=dasboard.objects.filter(tipoextraccion='Acopio').values('municipio', 'vereda', 'LL_Maximo')
    #Filtros para zona: Norte, Sur, Oriente y Centro
    ll_norte=dasboard.objects.filter(zona='Norte').values('municipio', 'vereda', 'LL_Maximo')
    ll_sur=dasboard.objects.filter(zona='Sur').values('municipio', 'vereda', 'LL_Maximo')
    ll_oriente=dasboard.objects.filter(zona='Oriente').values('municipio', 'vereda', 'LL_Maximo')
    ll_centro=dasboard.objects.filter(zona='Centro').values('municipio', 'vereda', 'LL_Maximo')
    #arrays para gráficar ll con su filtro: rio, cantera y acopio
    #completo ll
    array_objetos_ll=[]
    for dato in ll:
        x= f"{dato['municipio']}--{dato['vereda']}"
        y= dato['LL_Maximo']
        objeto={"x":x, "y":y}
        array_objetos_ll.append(objeto)
    #1.Rio
    array_objetos_ll_rio=[]
    for dato in ll_rio:
        x= f"{dato['municipio']}--{dato['vereda']}"
        y= dato['LL_Maximo']
        objeto={"x":x, "y":y}
        array_objetos_ll_rio.append(objeto)
    #2.Cantera
    array_objetos_ll_cantera=[]
    for dato in ll_cantera:
        x= f"{dato['municipio']}--{dato['vereda']}"
        y= dato['LL_Maximo']
        objeto={"x":x, "y":y}
        array_objetos_ll_cantera.append(objeto)
    #3.Acopio
    array_objetos_ll_acopio=[]
    for dato in ll_acopio:
        x= f"{dato['municipio']}--{dato['vereda']}"
        y= dato['LL_Maximo']
        objeto={"x":x, "y":y}
        array_objetos_ll_acopio.append(objeto)
    #4.Norte
    array_objetos_ll_norte=[]
    for dato in ll_norte:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['LL_Maximo']
        objeto={"x":x, "y":y}
        array_objetos_ll_norte.append(objeto)
    #5.Sur
    array_objetos_ll_sur=[]
    for dato in ll_sur:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['LL_Maximo']
        objeto={"x":x, "y":y}
        array_objetos_ll_sur.append(objeto)
    #6.Oriente
    array_objetos_ll_oriente=[]
    for dato in ll_oriente:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['LL_Maximo']
        objeto={"x":x, "y":y}
        array_objetos_ll_oriente.append(objeto)
    # 7.Centro 
    array_objetos_ll_centro=[]
    for dato in ll_centro:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['LL_Maximo']
        objeto={"x":x, "y":y}
        array_objetos_ll_centro.append(objeto)
    #Convertimos a Json
    grafica2=(json.dumps(array_objetos_ll))
    grafica2_ll_rio=(json.dumps(array_objetos_ll_rio))
    grafica2_ll_cantera=(json.dumps(array_objetos_ll_cantera))
    grafica2_ll_acopio=(json.dumps(array_objetos_ll_acopio))
    grafica2_ll_norte=(json.dumps(array_objetos_ll_norte))
    grafica2_ll_sur=(json.dumps(array_objetos_ll_sur))
    grafica2_ll_oriente=(json.dumps(array_objetos_ll_oriente))
    grafica2_ll_centro=(json.dumps(array_objetos_ll_centro))
    #-----------------//-------------------
    #2.Filtros para IP
    ip=dasboard.objects.all().values('municipio','vereda', 'IP')
    ip_rio=dasboard.objects.filter(tipoextraccion='Rio').values('municipio', 'vereda', 'IP')
    ip_cantera=dasboard.objects.filter(tipoextraccion='Cantera').values('municipio', 'vereda', 'IP')
    ip_acopio=dasboard.objects.filter(tipoextraccion='Acopio').values('municipio', 'vereda', 'IP')
    #Filtros para zona: Norte, Sur, Oriente y Centro
    ip_norte=dasboard.objects.filter(zona='Norte').values('municipio', 'vereda','IP')
    ip_sur=dasboard.objects.filter(zona='Sur').values('municipio', 'vereda','IP')
    ip_oriente=dasboard.objects.filter(zona='Oriente').values('municipio', 'vereda','IP')
    ip_centro=dasboard.objects.filter(zona='Centro').values('municipio', 'vereda','IP')
    #arrays para gráficar ip con su filtro: rio, cantera y acopio, norte, sur, oriente y centro
    #completo ip
    array_objetos_ip=[]
    for dato in ip:
        x= f"{dato['municipio']}--{dato['vereda']}"
        y= dato['IP']
        objeto={"x":x, "y":y}
        array_objetos_ip.append(objeto)
    #1.Rio
    array_objetos_ip_rio=[]
    for dato in ip_rio:
        x= f"{dato['municipio']}--{dato['vereda']}"
        y= dato['IP']
        objeto={"x":x, "y":y}
        array_objetos_ip_rio.append(objeto)
    #2.Cantera
    array_objetos_ip_cantera=[]
    for dato in ip_cantera:
        x= f"{dato['municipio']}--{dato['vereda']}"
        y= dato['IP']
        objeto={"x":x, "y":y}
        array_objetos_ip_cantera.append(objeto)
    #3.Acopio
    array_objetos_ip_acopio=[]
    for dato in ip_acopio:
        x= f"{dato['municipio']}--{dato['vereda']}"
        y= dato['IP']
        objeto={"x":x, "y":y}
        array_objetos_ip_acopio.append(objeto)
    #4.Norte
    array_objetos_ip_norte=[]
    for dato in ip_norte:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['IP']
        objeto={"x":x, "y":y}
        array_objetos_ip_norte.append(objeto)
    #5.Sur
    array_objetos_ip_sur=[]
    for dato in ip_sur:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['IP']
        objeto={"x":x, "y":y}
        array_objetos_ip_sur.append(objeto)
    #6.Oriente
    array_objetos_ip_oriente=[]
    for dato in ip_oriente:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['IP']
        objeto={"x":x, "y":y}
        array_objetos_ip_oriente.append(objeto)
    #7.Centro
    array_objetos_ip_centro=[]
    for dato in ip_centro:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['IP']
        objeto={"x":x, "y":y}
        array_objetos_ip_centro.append(objeto)

    #Convertimos a Json
    grafica3=(json.dumps(array_objetos_ip))
    grafica3_ip_rio=(json.dumps(array_objetos_ip_rio))
    grafica3_ip_cantera=(json.dumps(array_objetos_ip_cantera))
    grafica3_ip_acopio=(json.dumps(array_objetos_ip_acopio))
    grafica3_ip_norte=(json.dumps(array_objetos_ip_norte))
    grafica3_ip_sur=(json.dumps(array_objetos_ip_sur))
    grafica3_ip_oriente=(json.dumps(array_objetos_ip_oriente))
    grafica3_ip_centro=(json.dumps(array_objetos_ip_centro))
    #-----------------//-------------------
    #3.Filtros para Dureza
    dureza=dasboard.objects.all().values('municipio','vereda', 'Dureza_maquina_angeles')
    dureza_rio=dasboard.objects.filter(tipoextraccion='Rio').values('municipio', 'vereda', 'Dureza_maquina_angeles')
    dureza_cantera=dasboard.objects.filter(tipoextraccion='Cantera').values('municipio', 'vereda', 'Dureza_maquina_angeles')
    dureza_acopio=dasboard.objects.filter(tipoextraccion='Acopio').values('municipio', 'vereda', 'Dureza_maquina_angeles')
    #Filtros para zona: norte, sur, oriente, centro
    dureza_norte=dasboard.objects.filter(zona='Norte').values('municipio', 'vereda', 'Dureza_maquina_angeles')
    dureza_sur=dasboard.objects.filter(zona='Sur').values('municipio', 'vereda', 'Dureza_maquina_angeles')
    dureza_oriente=dasboard.objects.filter(zona='Oriente').values('municipio', 'vereda', 'Dureza_maquina_angeles')
    dureza_centro=dasboard.objects.filter(zona='Centro').values('municipio', 'vereda', 'Dureza_maquina_angeles')
    #arrays para gráficar dureza con su filtro: rio, cantera y acopio
    #completo ll
    array_objetos_dureza=[]
    for dato in dureza:
        x= f"{dato['municipio']}--{dato['vereda']}"
        y= dato['Dureza_maquina_angeles']
        objeto={"x":x, "y":y}
        array_objetos_dureza.append(objeto)
    #1.Rio
    array_objetos_dureza_rio=[]
    for dato in dureza_rio:
        x= f"{dato['municipio']}--{dato['vereda']}"
        y= dato['Dureza_maquina_angeles']
        objeto={"x":x, "y":y}
        array_objetos_dureza_rio.append(objeto)
    #2.Cantera
    array_objetos_dureza_cantera=[]
    for dato in dureza_cantera:
        x= f"{dato['municipio']}--{dato['vereda']}"
        y= dato['Dureza_maquina_angeles']
        objeto={"x":x, "y":y}
        array_objetos_dureza_cantera.append(objeto)
    #3.Acopio
    array_objetos_dureza_acopio=[]
    for dato in dureza_acopio:
        x= f"{dato['municipio']}--{dato['vereda']}"
        y= dato['Dureza_maquina_angeles']
        objeto={"x":x, "y":y}
        array_objetos_dureza_acopio.append(objeto)
    #4.Norte
    array_objetos_dureza_norte=[]
    for dato in dureza_norte:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['Dureza_maquina_angeles']
        objeto={"x":x, "y":y}
        array_objetos_dureza_norte.append(objeto)
    #5.Sur
    array_objetos_dureza_sur=[]
    for dato in dureza_sur:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['Dureza_maquina_angeles']
        objeto={"x":x, "y":y}
        array_objetos_dureza_sur.append(objeto)
    #6.Oriente
    array_objetos_dureza_oriente=[]
    for dato in dureza_oriente:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['Dureza_maquina_angeles']
        objeto={"x":x, "y":y}
        array_objetos_dureza_oriente.append(objeto)
    #7.Centro
    array_objetos_dureza_centro=[]
    for dato in dureza_centro:
        x=f"{dato['municipio']}-{dato['vereda']}"
        y=dato['Dureza_maquina_angeles']
        objeto={"x":x, "y":y}
        array_objetos_dureza_centro.append(objeto)
    #Convertimos a Json
    grafica4=(json.dumps(array_objetos_dureza))
    grafica4_dureza_rio=(json.dumps(array_objetos_dureza_rio))
    grafica4_dureza_cantera=(json.dumps(array_objetos_dureza_cantera))
    grafica4_dureza_acopio=(json.dumps(array_objetos_dureza_acopio))
    grafica4_dureza_norte=(json.dumps(array_objetos_dureza_norte))
    grafica4_dureza_sur=(json.dumps(array_objetos_dureza_sur))
    grafica4_dureza_oriente=(json.dumps(array_objetos_dureza_oriente))
    grafica4_dureza_centro=(json.dumps(array_objetos_dureza_centro))
    #------//-----------------MAPA CON LEAFLET PARA PRODUCCION----------------------------------------------
    municipios=produccion.objects.all()
    data=[]
    for i in municipios:
        row = {
            'municipio': i.MUNICIPIO, 
            'departamento': i.DEPARTAMENTO, 
            'produccion cafe': i.CAFE, 
            'produccion caña': i.CAÑA, 
            'produccion pino y eucalipto': i.PINO_Y_EUCALIPTO, 
            'produccion fique': i.FIQUE, 
            'latitud': float(i.LATITUD), 
            'longitud': float(i.LONGITUD)
        }
        data.append(row)
    # Convertir a GeoJSON
    geojson_obj = geojson.FeatureCollection([
    geojson.Feature(
        geometry=geojson.Point((d["longitud"], d["latitud"])),
        properties={
            "municipio": d["municipio"],
            "departamento": d["departamento"],
            "produccion_cafe": d["produccion cafe"],
            "produccion_caña": d["produccion caña"],
            "produccion_pino_y_eucalito": d["produccion pino y eucalipto"],
            "produccion_fique": d["produccion fique"],
            "id": d["municipio"]
        }
    ) for d in data
    ])
    mapa = geojson.dumps(geojson_obj)
    #------//------------------------DIAGRAMA DE PASTEL PRODUCCION---------------------------------------
    diagrama=produccion.objects.all()
    #resultado suma de c/prod. // Sí, al utilizar el método aggregate(Sum('CAFE')), Django genera automáticamente una clave en el diccionario resultante con el formato 'CAFE__sum'. Esto se debe a que el método aggregate realiza una operación de agregación, en este caso la suma, y por lo tanto necesita un nombre para el resultado de dicha operación. En el ejemplo que mencionaste, el resultado sería un diccionario con una única clave 'CAFE__sum' y su valor correspondiente a la suma de la columna 'CAFE' de todas las filas de la tabla. Para acceder al valor de la suma, se debe utilizar la sintaxis de diccionario, por ejemplo, cafecount['CAFE__sum'].
    cafecount=produccion.objects.aggregate(Sum('CAFE'))['CAFE__sum'] 
    cañacount=produccion.objects.aggregate(Sum('CAÑA'))['CAÑA__sum']
    pecount=produccion.objects.aggregate(Sum('PINO_Y_EUCALIPTO'))['PINO_Y_EUCALIPTO__sum']
    fiquecount=produccion.objects.aggregate(Sum('FIQUE'))['FIQUE__sum']
    #definimos la estructura JSON del dicc con el resultado de la suma para cada uno
    data={
        'value':str(cafecount),
        'value2':str(cañacount),
        'value3':str(pecount),
        'value4':str(fiquecount),
    }
    data_json=json.dumps(data)
    # for j in diagrama:
    #     cafe.append(j.CAFE)
    #     caña.append(j.CAÑA)
    #     pinoyeucalipto.append(j.PINO_Y_EUCALIPTO)
    #     fique.append(j.FIQUE)
    #-----------------//-------------------
    contexto={
        #solo para lectura
        'cantera':cantera, 
        'rio':rio, 
        'acopio':acopio, 
        'producciones':producciones, 
        'ensayos':resultados,
        #graficas cbr
        'grafica1':grafica1,
        'grafica1_cbr_rio':grafica1_cbr_rio,
        'grafica1_cbr_cantera':grafica1_cbr_cantera, 
        'grafica1_cbr_acopio':grafica1_cbr_acopio,
        'grafica1_cbr_norte':grafica1_cbr_norte,
        'grafica1_cbr_sur':grafica1_cbr_sur,
        'grafica1_cbr_oriente':grafica1_cbr_oriente,
        'grafica1_cbr_centro':grafica1_cbr_centro,
        #graficas ll
        'grafica2':grafica2,
        'grafica2_ll_rio':grafica2_ll_rio,
        'grafica2_ll_cantera':grafica2_ll_cantera, 
        'grafica2_ll_acopio':grafica2_ll_acopio,
        'grafica2_ll_norte':grafica2_ll_norte,
        'grafica2_ll_sur':grafica2_ll_sur,
        'grafica2_ll_oriente':grafica2_ll_oriente,
        'grafica2_ll_centro':grafica2_ll_centro, 
        #graficas ip
        'grafica3':grafica3,
        'grafica3_ip_rio':grafica3_ip_rio,
        'grafica3_ip_cantera':grafica3_ip_cantera, 
        'grafica3_ip_acopio':grafica3_ip_acopio,
        'grafica3_ip_norte':grafica3_ip_norte,
        'grafica3_ip_sur':grafica3_ip_sur,
        'grafica3_ip_oriente':grafica3_ip_oriente,
        'grafica3_ip_centro':grafica3_ip_centro, 
        #graficas dureza
        'grafica4':grafica4,
        'grafica4_dureza_rio':grafica4_dureza_rio,
        'grafica4_dureza_cantera':grafica4_dureza_cantera, 
        'grafica4_dureza_acopio':grafica4_dureza_acopio,
        'grafica4_dureza_norte':grafica4_dureza_norte,
        'grafica4_dureza_sur':grafica4_dureza_sur,
        'grafica4_dureza_oriente':grafica4_dureza_oriente,
        'grafica4_dureza_centro':grafica4_dureza_centro, 
        #mapa
        'mapaproduccion':mapa,
        #diagrama de pastel
        'datos':data_json,
        }
    return render(request, 'Dashboard/dashboard.html', contexto)

  