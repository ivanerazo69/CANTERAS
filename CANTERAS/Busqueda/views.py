from django.shortcuts import render, HttpResponse
from Busqueda.models import Fuente_Inicial
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.express as px
import pandas as pd
import folium
import requests
from folium import plugins
from folium.plugins import Fullscreen
from django.db.models import Q

#----------------------------------------------------------------------------------------------
def graficaCBR(request):
    fuentes_cbr = Fuente_Inicial.objects.exclude(CBR=None) #sentencia devuelve solo aquellos objetos Fuente_Inicial donde el campo CBR no es nulo. Sí, exacto. En este caso, se refiere a un valor de la columna CBR que no tiene un valor asignado, es decir, está vacío o nulo. La sentencia .exclude(CBR=None) se utiliza para excluir de la consulta aquellos registros donde el valor de la columna CBR sea nulo.
    municipios = []
    valores_cbr = []
    #excepción que se genera cuando se intenta convertir una cadena vacía en un número flotante, lo cual ocurre cuando el valor del campo CBR en la base de datos es una cadena vacía en lugar de un número.
    #En la sentencia try, se intenta convertir el valor del campo CBR a un número flotante. Si se puede hacer esta conversión, se agrega el valor y el municipio a las respectivas listas. Si no se puede hacer la conversión porque el valor es una cadena vacía, la excepción ValueError se maneja con la sentencia except, que simplemente pasa al siguiente elemento de la iteración sin agregar nada a las listas. De esta manera, se evita que se produzca un error al intentar graficar una cadena vacía como un número.
    for fuente in fuentes_cbr:
        try:
            valor_cbr = float(fuente.CBR)
            municipios.append(fuente.municipio)
            valores_cbr.append(valor_cbr)
        except (ValueError, TypeError):
            pass
    fig = go.Figure(data=go.Scatter(x=municipios, y=valores_cbr, mode='markers'))
    fig.update_layout(title='Valores de CBR por Municipio',
                    xaxis_title='Municipios',
                    yaxis_title='Valores de CBR')
    #plot_html4 = fig.to_html(full_html=False)
    #return HttpResponse(plot_html4)
    plot_div = plot(fig, auto_open=False, output_type='div')
    return plot_div

def busqueda(request):
    fuentes=Fuente_Inicial.objects.all()
    #llamamos a la vista o la función para que logremos pasar por contexto.
    grafica = graficaCBR(request)
    return render(request, 'Busqueda/busqueda.html', {"busquedas":fuentes, "plot_html4": grafica})

#---------------------------------Buscador en página principal-------------------------------------
def busquedaFuente(request):
    query = request.GET.get('q')
    if query:
        fuentes = Fuente_Inicial.objects.filter(Q(municipio__icontains=query) | Q(tipoextraccion__icontains=query) | Q(zona__icontains=query) | Q(nombre_fuente__icontains=query)) 
    else:
        fuentes = Fuente_Inicial.objects.all()
    return render(request, 'Busqueda/busqueda.html', {'busquedas': fuentes})
#--------------------------------Gráficas:Fuentes y Estudios---------------------------------
def grafica_fuentes(request):
    fuentes=Fuente_Inicial.objects.all()
    fig = go.Figure()
    df = pd.DataFrame(list(fuentes.values()))
    conteo_municipios=df['municipio'].value_counts()
    fig = px.bar(conteo_municipios, x=conteo_municipios.index, y=conteo_municipios.values)
    plot_html=fig.to_html(full_html=False)
    #---------//---------
    # fig2 = go.Figure()
    # df2=pd.DataFrame(list(fuentes.values()))
    # conteo_estudios=df2['ESTUDIO_S_N'].value_counts()
    # fig2=px.bar(conteo_estudios, x=conteo_estudios.index, y=conteo_estudios.values)
    # plot_html2 = fig2.to_html(full_html=False)
    #---------//---------
    graficacbr=graficaCBR(request)
    
    return render(request, 'Busqueda/graficos.html', {'plot_html':plot_html, 'plot_html3':graficacbr})
#--------------------------------------Vista del MAPA--------------------------------------------------
#presentación del mapa en pantalla inicial
def mapa(request):
    fuentes=Fuente_Inicial.objects.all()
    if fuentes:
        initialMap = folium.Map(location=[fuentes[0].coordenada_Latitud, fuentes[0].coordenada_Longitud], zoom_start=11)
        folium.TileLayer(
        tiles='https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.jpg?access_token=pk.eyJ1IjoiaXZhbmVyYXpvIiwiYSI6ImNsZmljb21iODBlbTg0NHM1dW1xanV6YnUifQ.fMDSTRe4YiVBm_kWbbvarg',
        attr='Mapbox',
        name='Satellite', 
        ).add_to(initialMap)
        folium.TileLayer(tiles='Stamen Terrain').add_to(initialMap)
        folium.LayerControl().add_to(initialMap)
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
        folium.Marker([fuente.coordenada_Latitud, fuente.coordenada_Longitud], tooltip=f'Hola, esta es la cantera de nombre: {fuente.nombre_fuente}').add_to(initialMap)    
    
    context={'map':initialMap._repr_html_()}
    return render(request, 'Busqueda/mapa.html', context)

# esta función nos permite buscar en el mapa
def buscarMun(request):
    #opcion para obtener lista con valores:
    norte=list(Fuente_Inicial.objects.filter(zona='Norte').values_list('municipio', flat=True).distinct())
    sur=list(Fuente_Inicial.objects.filter(zona='Sur').values_list('municipio', flat=True).distinct())
    centro=list(Fuente_Inicial.objects.filter(zona='Centro').values_list('municipio', flat=True).distinct())
    oriente=list(Fuente_Inicial.objects.filter(zona='Oriente').values_list('municipio', flat=True).distinct())
    municipioslista=list(Fuente_Inicial.objects.values_list('municipio', flat=True).distinct())
    # municipioslista=[f"{municipio}" for municipio in municipiolista]
    # municipios_veredas=list(dasboard.objects.values_list('municipio','vereda').distinct())
    # municipios=[f"{municipio}-{vereda}" for municipio, vereda in municipios_veredas]
    
    fuetes=Fuente_Inicial.objects.all()
    if request.method == 'POST':
        municipio=request.POST.get('municipio')
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')
        zona = request.POST.get('zona')
        if municipio:
            fuentes=Fuente_Inicial.objects.filter(municipio__icontains=municipio)
        elif latitud and longitud:
            fuentes=Fuente_Inicial.objects.filter(coordenada_Latitud=latitud, coordenada_Longitud=longitud)
        elif zona:
            if zona=='Cantera':
                fuentes=Fuente_Inicial.objects.filter(tipoextraccion='Cantera')
            elif zona=='Rio':
                fuentes=Fuente_Inicial.objects.filter(tipoextraccion='Rio')
            elif zona=='Acopio':
                fuentes=Fuente_Inicial.objects.filter(tipoextraccion='Acopio')
            elif zona=='CDT':
                fuentes=Fuente_Inicial.objects.filter(pr='nan')
            elif zona=='Base':
                fuentes=Fuente_Inicial.objects.filter(CBR='NaN')
            else:
                fuentes=Fuente_Inicial.objects.filter(zona__icontains=zona)
        else:
            fuentes = Fuente_Inicial.objects.all()
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

            for fuente in fuetes:
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
        
        
        context={'map':initialMap._repr_html_(), 
                'fuentes':fuentes,
                'municipioslista':municipioslista, 
                'norte':norte, 
                'sur':sur, 
                'centro':centro, 
                'oriente':oriente}

        return render(request, 'Busqueda/mapa.html',context)
    else:
        return mapa(request)

def procesos(request):
    return render(request, 'Busqueda/procesos.html')
    