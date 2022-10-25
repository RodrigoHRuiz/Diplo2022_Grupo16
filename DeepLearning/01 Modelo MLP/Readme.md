# Modelo MLP
## Detalle de los pasos seguidos
### Lectura de los datos
Los datos para el problema se dividen en tres conjuntos: train, validation y test.
A los fines prácticos de poder realizar el ajuste de hiperparámetros en un lapso de tiempo acorde a la disponibilidad de los recursos de cálculo disponibles, se programó la opción de tomar una muestra aleatoria del 10% de los conjuntos train y validation; siempre procurando mantener la distribución de clases del conjunto original.
Se grafican las 10 categorías con mayor frecuencia y las 10 con menor frecuencia, para cada uno de los conjuntos de datos. Como puede observarse, las muestras seleccionadas mantienen la distribución de los conjuntos originales.
Luego, el entrenamiento del modelo seleccionado como definitivo, será entrenado con todos los datos del conjunto train y se analizará el desempeño sobre todo el conjunto test.

### Creación de las clases dataset
Se preparon dos clases dataset, una para levantar todos los datos del lote y otra que lo hace en forma iterable, según las posibilidades de cómputo.

### Preprocesamiento de los títulos de las publicaciones
El preprocesamiento de los títulos se realizó utilizando las librerías Gensim y NLTK. Las tareas se ejecutan en el siguiente orden:
- Transformar todas las cadenas en minúsculas
- Eliminación de etiquetas de código del tipo <i></i>, <b></b>
- Separación por un espacio de cadenas alfanuméricas
- Reemplazo de signos de puntuación ASCII por espacios
- Eliminación de cualquier otro caracter que no sea letras o númemros
- Remoción de espacios múltiples
- Eliminación de dígitos numéricos
- Descarte de cadenas de longitud menor a 3



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
