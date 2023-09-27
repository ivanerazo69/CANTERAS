import numpy as np
from django.conf import settings
from pathlib import Path
from django.shortcuts import render
from Dashboard.models import dasboard
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import save_model
import matplotlib.pyplot as plt

#Función para evaluar los requisitos de un ensayo
def cumple_requisitos(ensayo):
    if (ensayo['Dureza_maquina_angeles']>50 and 
        4<ensayo['IP']<=9 and 
        ensayo['CBR']>=15): 
        return True
    else:
        return False

#Función para evaluar los requisitos de un ensayo
def cumple_requisitos(ensayo):
    if (ensayo['Dureza_maquina_angeles']>50 and 
        4<ensayo['IP']<=9 and 
        ensayo['CBR']>=15): 
        return True
    else:
        return False

# Cargar los datos desde la base de datos Django
datos_fuente = dasboard.objects.values('Dureza_maquina_angeles', 'IP', 'CBR')

# Etiquetar los datos según si cumplen o no con los requisitos 
y = np.array([cumple_requisitos(datos) for datos in datos_fuente])

# Convertir los datos a un arreglo de numpy
X = np.array([[datos_fuentes['Dureza_maquina_angeles'], datos_fuentes['IP'], datos_fuentes['CBR']] for datos_fuentes in datos_fuente])

# Construir el modelo de red neuronal
model = Sequential()
model.add(Dense(64, input_dim=3, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compilar el modelo
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Entrenar el modelo
model.fit(X, y, epochs=100, batch_size=32)

# Ruta de la carpeta para guardar el modelo (reemplaza 'ruta_absoluta' con la ruta real)
ruta_carpeta_modelo = Path('C:/Users/IVAN ERAZO/OneDrive - unicauca.edu.co/TRABAJO DE TESIS/SOFTWARE_CANTERAS/CANTERAS') /  'modelo_entrenado'
# Crear la carpeta si no existe
ruta_carpeta_modelo.mkdir(parents=True, exist_ok=True)

# Guardar el modelo en la nueva carpeta
ruta_archivo_modelo = ruta_carpeta_modelo / 'modelofff.keras'
model.save(str(ruta_archivo_modelo))

#/////////////////////////        

# Imprimir las métricas de entrenamiento (pérdida y precisión) de cada época
print("Pérdida por época:", history.history['loss'])
print("Precisión por época:", history.history['accuracy'])

# Visualizar las métricas de entrenamiento
loss = history.history['loss']
accuracy = history.history['accuracy']
epochs = range(1, len(loss) + 1)

# Gráfica de pérdida
plt.plot(epochs, loss, 'b', label='Pérdida')
plt.title('Pérdida durante el entrenamiento')
plt.xlabel('Época')
plt.ylabel('Pérdida')
plt.legend()
plt.show()

# Gráfica de precisión
plt.plot(epochs, accuracy, 'r', label='Precisión')
plt.title('Precisión durante el entrenamiento')
plt.xlabel('Época')
plt.ylabel('Precisión')
plt.legend()
plt.show()
