# Modelo MLP
## Detalle de los pasos seguidos
### Lectura de los datos
Los datos para el problema se dividen en tres conjuntos: train, validation y test.
A los fines prácticos de poder realizar el ajuste de hiperparámetros en un lapso de tiempo acorde a la disponibilidad de los recursos de cálculo disponibles, se programó la opción de tomar una muestra aleatoria del 10% de los conjuntos train y validation; siempre procurando mantener la distribución de clases del conjunto original.
Se grafican las 10 categorías con mayor frecuencia y las 10 con menor frecuencia, para cada uno de los conjuntos de datos. Como puede observarse, las muestras seleccionadas mantienen la distribución de los conjuntos originales; y se asegura que dentro de cada conjunto estén las 632 categorías. Es importante también resaltar que los 3 conjuntos están muy desbalanceados.
![graficos clases](https://github.com/RodrigoHRuiz/Diplo2022_Grupo16/blob/main/DeepLearning/images/graficos_clases.png?raw=true)
Luego, el entrenamiento del modelo seleccionado como definitivo, será entrenado con todos los datos del conjunto train y se analizará el desempeño sobre todo el conjunto test.

### Creación de las clases dataset
Se preparon dos clases dataset, una para levantar todos los datos del lote y otra que lo hace en forma iterable, según las posibilidades de cómputo.

### Preprocesamiento de los títulos de las publicaciones
El preprocesamiento de los títulos se realizó utilizando las librerías Gensim y NLTK. Las tareas se ejecutan en el siguiente orden:
- Transformar todas las cadenas en minúsculas
- Eliminar etiquetas de código del tipo <i></i>, <b></b>
- Separar por un espacio de cadenas alfanuméricas
- Reemplazar signos de puntuación ASCII por espacios
- Eliminar cualquier otro caracter que no sea letras o númemros
- Remover espacios múltiples
- Eliminar dígitos numéricos
- Descartar las cadenas de longitud menor a 3
Una vez generado el diccionario de palabras, se eliminan de este las palabras vacías (o stopwords) del listado predefinido para español en la librería NLTK. Esto es para propiciar que en diccionario aparezcan palabras que puedan aportar información relevante.
Luego, se incluyen dos tokens especiales. Uno para las palabras desconocidas (1) y otro para el relleno al ajustar el tamaño de las cadenas (0).
Por último, se codifican las categorías con un índice, por orden de aparición. En este caso se cuenta con 632 categrías diferentes.

### PadSequences y Dataloaders

### Modelo baseline

### Modelo para ajuste de los hiperparámetros

## Experimentos

### Mejor modelo

## Resultados y performance sobre el conjunto Test



## Archivos respaldo
<a href="https://drive.google.com/file/d/1vEZYwQ7jsEyreZxcG-eyvMbKKxAlMF1Y/view?usp=sharing">Experimentos MLflow</a>
<br>
<a href="https://drive.google.com/file/d/16KqVWlnR8qIdedh30F0KK5i2K9OZjc6A/view?usp=sharing">Parámetros del mejor modelo</a>
