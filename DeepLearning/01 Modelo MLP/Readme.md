# Modelo MLP
## Detalle de los pasos seguidos
### Lectura de los datos
Los datos para el problema se dividen en tres conjuntos: train, validation y test.
A los fines prácticos de poder realizar el ajuste de hiperparámetros en un lapso de tiempo acorde a la disponibilidad de los recursos de cálculo disponibles, se programó la opción de tomar una muestra aleatoria del 10% de los conjuntos train y validation; siempre procurando mantener la distribución de clases del conjunto original.
Se grafican las 10 categorías con mayor frecuencia y las 10 con menor frecuencia, para cada uno de los conjuntos de datos. Como puede observarse, las muestras seleccionadas mantienen la distribución de los conjuntos originales; y se asegura que dentro de cada conjunto estén las 632 categorías. Es importante también resaltar que los 3 conjuntos están muy desbalanceados.
![graficos clases](https://github.com/RodrigoHRuiz/Diplo2022_Grupo16/blob/main/DeepLearning/images/graficos_clases.png?raw=true)
Luego, el entrenamiento del modelo seleccionado como definitivo, será entrenado con todos los datos del conjunto train y se analizará el desempeño sobre todo el conjunto test.

### Creación de las clases dataset
Se crearon dos clases dataset, una para levantar todos los datos del lote y otra que lo hace en forma iterable, según las posibilidades de cómputo.

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
Se creó una clase PadSequences para iguales el tamaño de los datos con los que será alimentada la red.
Además, se utilizan los dataloaders de Pytorch para pasar los datos por lotes a la red.

### Modelo baseline
Se diseñó un modelo simple con una capa de emeding, luego una capa oculta con función de activación relu y la capa de salida. La función de pérdida utilizada para todo el trabajo fue CrossEntropyLoss, apropiada para problemas de clasificación muticlase. Además, se optó por utiilizar Adam como algoritmo de optimización.
Por una cuestión de capacidad de procesamiento todos los modelos fueron entrenados en 5 épocas. Se intentó con 10 épocas para poder tener un rango más amplio y evaluar si la función de pérdida podía mostrar signos de sobreajuste; pero esto no fue posible porque en el 90% de los casos el proceso no puede concluir por falta de recursos, se detenía el kernel.
La métrica utilizada para evaluar los modelos fue balanced accuracy.
El modelo baseline alcanzó un resultado de 67.4%, y será la línea base para comprar con otras arquitecturas de red e hiperparámetros.

### Modelo para ajuste de los hiperparámetros
Para la búsqueda de los mejores hiperparámetro se agregó una capa oculta adicional y dropout a la red. Además, se definió una función para el entrenamiento y evaluación de los modelos que recibe como parámetros el tamaño de la primera y segunda capa oculta, la propoción para el dropout, la función de activación, el algoritmo de optimización, tasa de aprendizaje, parámetro de regularización, épocas y la opción de guardar los parámetros del modelo entrenado.

## Experimentos
Todos los experimentos fueron registrados con MLflow para poder comprar los modelos y optener las gráficas de pérdida para entrenamiento y evaluación.
Dada la elección de posibles hiperparámetros, había que evaluar 64 modelos. Para evitar el riesgo de perder el proceso en algún punto intermedio, se dividió en 4 etapas, es decir de a 16 modelos por vez.
A continuación se puede ver la tabla de registros de MLflow con los primeros resultados, ordenados por la métrica.
![registros mlflows](https://github.com/RodrigoHRuiz/Diplo2022_Grupo16/blob/main/DeepLearning/images/mlflow.png?raw=true)

### Mejor modelo
El modelo seleccionado como definitivo es el que puede verse seleccionado en la imagen anterior. Su elección se debió a que, comparado con los modelos más arriba, la diferencia en la métrica no era significativa y esos otros modelos ya comenzaban a mostrar signos de sobreajuste antes de la 5ta época, como puede verse en la imagen que sigue:
![principio sobreajuste](https://github.com/RodrigoHRuiz/Diplo2022_Grupo16/blob/main/DeepLearning/images/loss_principio_sobreajuste.png?raw=true)
En cambio, las curvas de pérdida para el modelo seleccionado muestran una mejor situación:
![curvas mejor modelo](https://github.com/RodrigoHRuiz/Diplo2022_Grupo16/blob/main/DeepLearning/images/loss_mejor_,modelo.png?raw=true)

## Resultados y performance sobre el conjunto Test



## Archivos respaldo
<a href="https://drive.google.com/file/d/1vEZYwQ7jsEyreZxcG-eyvMbKKxAlMF1Y/view?usp=sharing">Experimentos MLflow</a>
<br>
<a href="https://drive.google.com/file/d/16KqVWlnR8qIdedh30F0KK5i2K9OZjc6A/view?usp=sharing">Parámetros del mejor modelo</a>
