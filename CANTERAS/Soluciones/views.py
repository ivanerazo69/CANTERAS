from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from Soluciones.models import franjas
from Soluciones.models import grafo
from Dashboard.models import dasboard 
from django.views.generic import TemplateView
from django.http.response import JsonResponse
import json
import folium
import requests
from folium import plugins
from folium.plugins import Fullscreen
import plotly.graph_objects as go
import networkx as nx
import os
import sys

#/***************************************************************************************/
#función para el grafo y el algoritmo de disjktra
def generar_grafica(request):
    # Obtener los datos del modelo "Grafo"
    datos = grafo.objects.all()

    # Crear el grafo vacío
    G = nx.Graph()
    #Crear un diccionario para almacenar las etiquetas de los NODOS
    etiquetas={}

    # Agregar los nodos y las aristas al grafo y adicional las etiquetas de los nodos
    for dato in datos:
        G.add_edge(dato.NODO, dato.CONEXION, weight=int(dato.DISTANCIA))
        # Agregar etiquetas a los nodos desde la base de datos
        etiquetas[dato.NODO] = dato.NODO  # Aquí se asume que el nombre de nodo es la etiqueta
         # Asegúrate de que el atributo "weight" esté configurado correctamente en las aristas
        G[dato.NODO][dato.CONEXION]["weight"] = dato.DISTANCIA
    
    # Asignar las etiquetas a los nodos
    nx.set_node_attributes(G, etiquetas, 'label')

    #ruta mínima
    ruta_mas_corta = ''
    distancias_entre_nodos=''
    distancias_tiempo = ''
    resultado_horas=''
    if request.method == 'POST':
        origen = request.POST.get('origen')
        destino = request.POST.get('destino')
        # Calcular la ruta más corta utilizando el algoritmo de Dijkstra
        ruta_mas_corta = nx.dijkstra_path(G, origen, destino)
                       
        # Obtener las distancias entre cada par de nodos en la ruta mínima
        distancias_entre_nodos = {}
        for i in range(len(ruta_mas_corta) - 1):
            u = ruta_mas_corta[i]
            v = ruta_mas_corta[i + 1]
            distancia = G[u][v]["weight"]
            distancias_entre_nodos[f'Distancia entre {u} y {v}'] = distancia
        
        # Calcular el tiempo en función de la velocidad constante
        velocidad = 15  # Velocidad constante en Km/h
        tiempo=float(0.0)
        suma_tiempo=0 #Inicializamos en cero
        distancias_tiempo = []
        for key, distancia in distancias_entre_nodos.items():  #recordemos que key y distancia son var
            tiempo = round(distancia / velocidad, 2)
            suma_tiempo+=tiempo #Contador
            distancias_tiempo.append({
                "descripcion": key,
                "distancia": distancia,
                "velocidad": velocidad,
                "tiempo": tiempo,
            })
        resultado_horas=round(suma_tiempo,2)                
        # Ahora distancias_entre_nodos contiene las distancias entre cada par de nodos en la ruta más corta
        print(distancias_entre_nodos)

    # Generar la visualización del grafo utilizando Plotly
    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='black'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    # En la generación de la visualización del grafo
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',  # Agregar texto a los markers
        hoverinfo='text',
        text=list(G.nodes),  # Usar los nombres de los nodos como texto
        textposition='bottom center',  # Posición del texto
        marker=dict(
            showscale=False,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2)) 

    # Crear Scatter para las aristas
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='black'),
        hoverinfo='text',  # Mostrar información al pasar el mouse
        # Mostrar las distancias en el texto
        text=[G[u][v]["weight"] for u, v in G.edges()],
        mode='lines')

    #pintar nodos que contenga la ruta mínima
    # Crear una lista vacía para los colores de los nodos
    node_colors = []

    # Recorrer los nodos y asignarles un color
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        if node in ruta_mas_corta:
            node_colors.append('#FF0000')  # Asignar color rojo a los nodos de la ruta mínima
        else:
            node_colors.append('#FFFFFF')  # Asignar color blanco por defecto

    # Asignar la lista de colores a la propiedad 'color' del 'node_trace'
    node_trace['marker']['color'] = node_colors

    # Crear Figure que contiene ambos Scatter
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Grafo',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    # Guardar la figura en un archivo HTML temporal
    fig_path = "ProyectoWebApp/static/temp_graph.html"
    fig.write_html(fig_path)
    return {"fig_path": fig_path, 
            "ruta_mas_corta":ruta_mas_corta, 
            "distancias_entre_nodos":distancias_entre_nodos, 
            "distancias_tiempo":distancias_tiempo,
            "resultado_horas":resultado_horas,}
#/****************************************************************************************
        #vista para cargar y mostrar el archivo temp_graph.html
def mostrar_grafo(request):
    return redirect('/static/temp_graph.html')
#/****************************************************************************************
        #Función para generar el mapa el cuál mostrará los puntos de la ruta mínima
def mapa_ruta(request):
    fuentes=dasboard.objects.all()
    if fuentes:
        initialMap = folium.Map(location=[fuentes[0].coordenada_Latitud, fuentes[0].coordenada_Longitud], zoom_start=11)
        folium.TileLayer(
        tiles='https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.jpg?access_token=pk.eyJ1IjoiaXZhbmVyYXpvIiwiYSI6ImNsZmljb21iODBlbTg0NHM1dW1xanV6YnUifQ.fMDSTRe4YiVBm_kWbbvarg',
        attr='Mapbox',
        name='Satellite', 
        ).add_to(initialMap)
        folium.TileLayer(tiles='Stamen Terrain').add_to(initialMap)
        folium.LayerControl().add_to(initialMap)
        # Agregando el plugin de Fullscreen
        initialMap.add_child(Fullscreen(
        position='topleft',
        title='Expandir mapa',
        title_cancel='Salir de pantalla completa',
        force_separate_button=True))
        minimap=plugins.MiniMap().add_to(initialMap)

        for fuente in fuentes:
            folium.CircleMarker(location=[fuente.coordenada_Latitud, fuente.coordenada_Longitud], radius=1).add_to(initialMap)    
    else:
        initialMap = folium.Map(location=[fuentes[0].coordenada_Latitud, fuentes[0].coordenada_Longitud], zoom_start=11)
        folium.TileLayer(
        tiles='https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.jpg?access_token=pk.eyJ1IjoiaXZhbmVyYXpvIiwiYSI6ImNsZmljb21iODBlbTg0NHM1dW1xanV6YnUifQ.fMDSTRe4YiVBm_kWbbvarg',
        attr='Mapbox',
        name='Satellite', 
        ).add_to(initialMap)
        folium.TileLayer(tiles='Stamen Terrain').add_to(initialMap)
        folium.LayerControl().add_to(initialMap)
    
    for fuente in fuentes:
        popup_content = "<strong>Tipo de extracción:</strong> {0}<br>".format(fuente.tipoextraccion)
        popup_content += "<strong>Nombre de fuente:</strong> {0}<br>".format(fuente.nombre_fuente)
        popup_content += "<strong>Observación de fuente:</strong> {0}<br>".format(fuente.observacion_fuente)
        popup_content += "<strong>Otras observaciones:</strong> {0}<br>".format(fuente.otras_observaciones)
        popup_content += "<strong>Municipio:</strong> {0}<br>".format(fuente.municipio)
        popup_content += "<strong>Vereda:</strong> {0}<br>".format(fuente.vereda)
        popup_content += "<strong>Coordenada Longitud:</strong> {0}<br>".format((fuente.coordenada_Latitud))
        popup_content += "<strong>Coordenada Longitud:</strong> {0}<br>".format((fuente.coordenada_Longitud))
        if fuente.tipoextraccion == 'Cantera':
            icon=folium.Icon(color="red")
        elif fuente.tipoextraccion == 'Rio':
            icon=folium.Icon(color="green")
        elif fuente.tipoextraccion =='Acopio':
            icon=folium.Icon(color="blue")
        popup = folium.Popup(popup_content, max_width=300)  
        folium.Marker([fuente.coordenada_Latitud, fuente.coordenada_Longitud], tooltip=f' El nombre de la fuente es : {fuente.nombre_fuente}', popup=popup, icon=icon).add_to(initialMap)      
            
    return {'mapa':initialMap._repr_html_(),}
#/****************************************************************************************
        #vista general
def soluciones(request):
    #/---------------------------MUNICIPIOS----------------------------/
    municipios_veredas=list(dasboard.objects.values_list('municipio','vereda').distinct())
    municipios=[f"{municipio}-{vereda}" for municipio, vereda in municipios_veredas]
    #/---------------------------Gráficas de C/M----------------------------/
    #FranjaS:A-38 y A-25
    franja1=franjas.objects.all().values('tamiz','MSA38','MIA38')
    franja2=franjas.objects.all().values('tamiz','MSA25','MIA25')
    #A-38
    array_objeto_franja1=[]
    for dato in franja1:
        x=dato['tamiz']
        y=dato['MSA38']
        objeto={"x":x, "y":y}
        array_objeto_franja1.append(objeto)
    arraya_objeto_franja2=[]
    for dato in franja1:
        x=dato['tamiz']
        y=dato['MIA38']
        objeto={"x":x, "y":y}
        arraya_objeto_franja2.append(objeto)
    #A-25
    array_objeto_franja2_1=[]
    for dato in franja2:
        x=dato['tamiz']
        y=dato['MSA25']
        objeto={"x":x, "y":y}
        array_objeto_franja2_1.append(objeto)
    array_objeto_franja2_2=[]
    for dato in franja2:
        x=dato['tamiz']
        y=dato['MIA25']
        objeto={"x":x, "y":y}
        array_objeto_franja2_2.append(objeto)
    
    #Franjas de las 23 canteras
    franja3=franjas.objects.all().values('tamiz','TamboMa')
    franja4=franjas.objects.all().values('tamiz','TamboCh')
    franja5=franjas.objects.all().values('tamiz','MoralesSB')
    franja6=franjas.objects.all().values('tamiz','MoralesSC')
    franja7=franjas.objects.all().values('tamiz','TotoroSab')
    franja8=franjas.objects.all().values('tamiz','TotoroSA')
    franja9=franjas.objects.all().values('tamiz','RosasTr')
    franja10=franjas.objects.all().values('tamiz','RosasUf')
    franja11=franjas.objects.all().values('tamiz','BolivarSR')
    franja12=franjas.objects.all().values('tamiz','BolivarCol')
    franja13=franjas.objects.all().values('tamiz','Piendamo')
    franja14=franjas.objects.all().values('tamiz','PopayanBe')
    franja15=franjas.objects.all().values('tamiz','PopayanCer')
    franja16=franjas.objects.all().values('tamiz','LaSierra')
    franja17=franjas.objects.all().values('tamiz','SotaraHB')
    franja18=franjas.objects.all().values('tamiz','SotaraSR')
    franja19=franjas.objects.all().values('tamiz','CaldonoEs')
    franja20=franjas.objects.all().values('tamiz','CaldonoJa')
    franja21=franjas.objects.all().values('tamiz','VillaRicaBP')
    franja22=franjas.objects.all().values('tamiz','VillaRicaSB')
    franja23=franjas.objects.all().values('tamiz','Guachene')
    franja24=franjas.objects.all().values('tamiz','LaVegaCR')
    franja25=franjas.objects.all().values('tamiz','LaVegaUv')

    #arrays para x,y
    array_objeto1=[]
    array_objeto2=[]
    array_objeto3=[]
    array_objeto4=[]
    array_objeto5=[]
    array_objeto6=[]
    array_objeto7=[]
    array_objeto8=[]
    array_objeto9=[]
    array_objeto10=[]
    array_objeto11=[]
    array_objeto12=[]
    array_objeto13=[]
    array_objeto14=[]
    array_objeto15=[]
    array_objeto16=[]
    array_objeto17=[]
    array_objeto18=[]
    array_objeto19=[]
    array_objeto20=[]
    array_objeto21=[]
    array_objeto22=[]
    array_objeto23=[]

    for dato in franja3:
        x=dato['tamiz']
        y=dato['TamboMa']
        objeto={"x":x, "y":y}
        array_objeto1.append(objeto)
    for dato in franja4:
        x=dato['tamiz']
        y=dato['TamboCh']
        objeto={"x":x, "y":y}
        array_objeto2.append(objeto)
    for dato in franja5:
        x=dato['tamiz']
        y=dato['MoralesSB']
        objeto={"x":x, "y":y}
        array_objeto3.append(objeto)
    for dato in franja6:
        x=dato['tamiz']
        y=dato['MoralesSC']
        objeto={"x":x, "y":y}
        array_objeto4.append(objeto)
    for dato in franja7:
        x=dato['tamiz']
        y=dato['TotoroSab']
        objeto={"x":x, "y":y}
        array_objeto5.append(objeto)
    for dato in franja8:
        x=dato['tamiz']
        y=dato['TotoroSA']
        objeto={"x":x, "y":y}
        array_objeto6.append(objeto)
    for dato in franja9:
        x=dato['tamiz']
        y=dato['RosasTr']
        objeto={"x":x, "y":y}
        array_objeto7.append(objeto)
    for dato in franja10:
        x=dato['tamiz']
        y=dato['RosasUf']
        objeto={"x":x, "y":y}
        array_objeto8.append(objeto)
    for dato in franja11:
        x=dato['tamiz']
        y=dato['BolivarSR']
        objeto={"x":x, "y":y}
        array_objeto9.append(objeto)
    for dato in franja12:
        x=dato['tamiz']
        y=dato['BolivarCol']
        objeto={"x":x, "y":y}
        array_objeto10.append(objeto)
    for dato in franja13:
        x=dato['tamiz']
        y=dato['Piendamo']
        objeto={"x":x, "y":y}
        array_objeto11.append(objeto)
    for dato in franja14:
        x=dato['tamiz']
        y=dato['PopayanBe']
        objeto={"x":x, "y":y}
        array_objeto12.append(objeto)
    for dato in franja15:
        x=dato['tamiz']
        y=dato['PopayanCer']
        objeto={"x":x, "y":y}
        array_objeto13.append(objeto)
    for dato in franja16:
        x=dato['tamiz']
        y=dato['LaSierra']
        objeto={"x":x, "y":y}
        array_objeto14.append(objeto)
    for dato in franja17:
        x=dato['tamiz']
        y=dato['SotaraHB']
        objeto={"x":x, "y":y}
        array_objeto15.append(objeto)
    for dato in franja18:
        x=dato['tamiz']
        y=dato['SotaraSR']
        objeto={"x":x, "y":y}
        array_objeto16.append(objeto)
    for dato in franja19:
        x=dato['tamiz']
        y=dato['CaldonoEs']
        objeto={"x":x, "y":y}
        array_objeto17.append(objeto)
    for dato in franja20:
        x=dato['tamiz']
        y=dato['CaldonoJa']
        objeto={"x":x, "y":y}
        array_objeto18.append(objeto)
    for dato in franja21:
        x=dato['tamiz']
        y=dato['VillaRicaBP']
        objeto={"x":x, "y":y}
        array_objeto19.append(objeto)
    for dato in franja22:
        x=dato['tamiz']
        y=dato['VillaRicaSB']
        objeto={"x":x, "y":y}
        array_objeto20.append(objeto)
    for dato in franja23:
        x=dato['tamiz']
        y=dato['Guachene']
        objeto={"x":x, "y":y}
        array_objeto21.append(objeto)
    for dato in franja24:
        x=dato['tamiz']
        y=dato['LaVegaCR']
        objeto={"x":x, "y":y}
        array_objeto22.append(objeto)
    for dato in franja25:
        x=dato['tamiz']
        y=dato['LaVegaUv']
        objeto={"x":x, "y":y}
        array_objeto23.append(objeto)

    #transformación a json.
    grafica1=json.dumps(array_objeto_franja1)
    grafica2=json.dumps(arraya_objeto_franja2)
    grafica25_1=json.dumps(array_objeto_franja2_1)
    grafica25_2=json.dumps(array_objeto_franja2_2)
    grafica3=json.dumps(array_objeto1)
    grafica4=json.dumps(array_objeto2)
    grafica5=json.dumps(array_objeto3)
    grafica6=json.dumps(array_objeto4)
    grafica7=json.dumps(array_objeto5)
    grafica8=json.dumps(array_objeto6)
    grafica9=json.dumps(array_objeto7)
    grafica10=json.dumps(array_objeto8)
    grafica11=json.dumps(array_objeto9)
    grafica12=json.dumps(array_objeto10)
    grafica13=json.dumps(array_objeto11)
    grafica14=json.dumps(array_objeto12)
    grafica15=json.dumps(array_objeto13)
    grafica16=json.dumps(array_objeto14)
    grafica17=json.dumps(array_objeto15)
    grafica18=json.dumps(array_objeto16)
    grafica19=json.dumps(array_objeto17)
    grafica20=json.dumps(array_objeto18)
    grafica21=json.dumps(array_objeto19)
    grafica22=json.dumps(array_objeto20)
    grafica23=json.dumps(array_objeto21)
    grafica24=json.dumps(array_objeto22)
    grafica25=json.dumps(array_objeto23)

    #-----------------------------
    #Dijstrak
    #flat=true: para que se itere sobre una lista plana y no sobre una lista de tuplas
    datos2 = list(grafo.objects.values_list('NODO', flat=True).distinct())
    sitios = [fuente for fuente in datos2]
    # Obtener el contexto de la vista que genera la gráfica
    grafica_contexto=generar_grafica(request)
    # Acceder al valor de fig_path desde el contexto
    fig_path = grafica_contexto["fig_path"]
    #Acceder a la ruta mínima:
    ruta_mas_corta=grafica_contexto["ruta_mas_corta"]
    #Acceder a las distancias de los nodos
    distancias_entre_nodos=grafica_contexto["distancias_entre_nodos"]   
    #Accedemos a la lista de tiempos, velocidad y descripción del grafo
    distancias_tiempo=grafica_contexto["distancias_tiempo"]
    #Recuperamos la suma total de tiempo
    resultado_horas=grafica_contexto["resultado_horas"]
    #-----------------------------
    mapa_resultado=mapa_ruta(request)

    #/---------------------------CONTEXTO----------------------------/
    contexto={
        'municipios':municipios,
        'grafica1':grafica1,
        'grafica2':grafica2,
        'grafica25_1':grafica25_1,
        'grafica25_2':grafica25_2,
        'grafica3':grafica3,
        'grafica4':grafica4,
        'grafica5':grafica5,
        'grafica6':grafica6,
        'grafica7':grafica7,
        'grafica8':grafica8,
        'grafica9':grafica9,
        'grafica10':grafica10,
        'grafica11':grafica11,
        'grafica12':grafica12,
        'grafica13':grafica13,
        'grafica14':grafica14,
        'grafica15':grafica15,
        'grafica16':grafica16,
        'grafica17':grafica17,
        'grafica18':grafica18,
        'grafica19':grafica19,
        'grafica20':grafica20,
        'grafica21':grafica21,
        'grafica22':grafica22,
        'grafica23':grafica23,
        'grafica24':grafica24,
        'grafica25':grafica25,
        'datos':sitios,
        "fig_path": fig_path,
        "ruta_mas_corta":ruta_mas_corta,
        "distancias_entre_nodos":distancias_entre_nodos,
        "distancias_tiempo":distancias_tiempo,
        "resultado_horas":resultado_horas,
        'mapa_resultado':mapa_resultado,
    }
    return render(request, 'Soluciones/soluciones.html', contexto)





