# -*- coding: utf-8 -*-
"""Grupo 16 - Entregable NoSup.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TDBeOurxP0iMPMW9F5-8Z701N1cjTCmJ

**Diplomatura en Ciencia de Datos, Aprendizaje Automático y sus Aplicaciones**

**Aprendizaje No Supervisado**

*Edición 2022*


GRUPO 16 -Integrantes:
- Fernanda Borghello,
- Rodrigo Ruiz,
- Alfonsina Szpeiner

----

<img src='https://i.blogs.es/ca1b1c/fifa-22-1/1366_2000.jpeg' width="550" height="350">

# Trabajo práctico entregable

Utilizar la base de jugadores “players_22.csv” disponible en la página de Kaggle https://www.kaggle.com/datasets/stefanoleone992/fifa-22-complete-player-dataset . Considerar que la base 2022 no tiene el mismo formato que la base vista en clase, a los nombres de las variables se les agregó una keyword para identificar a qué tipo de habilidad corresponde.

Con la nueva base, realizar un análisis análogo al que realizamos en el cursado de la materia con los datos FIFA2019. Realice comentarios en cada parte (verbose=True ;))

1- Análisis exploratorio de la base.

2- Evaluación visual  e intuitiva de a dos variables numéricas por vez.

3- Uso de dos técnicas de clustering: por ejemplo k-medias, DBSCAN, mezcla de Gaussianas y/o alguna jerárquica. Elección justificada de hiper-parámetros

4- Evaluación y Análisis de los clusters encontrados.

5- Pregunta: ¿Se realizó alguna normalización o escalado de la base? ¿Por qué ?

6- Uso de alguna transformación (proyección, Embedding) para visualizar los resultados y/o usarla como preprocesado para aplicar alguna técnica de clustering.

#1) Inicialización del entorno

**IMPORTAMOS LIBRERIAS**
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as  plt
import seaborn as sns
# %matplotlib inline

#Para ver todas las columnas, elimino limitaciones de filas/columnas
pd.set_option('display.max_columns',100)
pd.set_option('display.max_rows',1000)
import itertools
import warnings
warnings.filterwarnings("ignore")
import io

from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans,MeanShift, AgglomerativeClustering
from sklearn import decomposition
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from scipy.cluster import hierarchy as  shc
from sklearn.mixture import GaussianMixture

"""**OBTENEMOS LOS DATOS**"""

url = 'https://raw.githubusercontent.com/RodrigoHRuiz/Diplo2022_Grupo16/main/05%20NoSup/players_22.csv'
df = pd.read_csv(url)
df.head(5)

"""#2) Análisis exploratorio de la base"""

print('Cantidad de variables Totales: ', len(df.columns))

df.describe().round(2)

df.describe().columns # variables numéricas

"""**SELECCIONAMOS LAS VARIABLES DE INTERÉS, CONSIDERANDO SOLO LAS QUE INDICAN DESTREZAS DE LOS JUGADORES**

Eliminamos las siguientes variables:

*   **sofifa_id, player_url, long_name:** ya que decidimos solo quedarnos con la variable short_name
*   **club_name, club_team_id, nationality_id, nationality_name, club_jersey_number, club_loaned_from, club_joined, club_contract_valid_until, nation_jersey_number, body_type, real_face, player_tags, player_traits, player_face_url, club_logo_url, club_flag_url, nation_logo_url, nation_flag_url:** ya que consideramos que estas variables no describen la habilidad del jugador.
*  **ls, st, rs, lw, lf, cf, rf, rw, lam, cam, ram, lm, lcm, cm, rcm, rm, lwb, ldm, cdm, rdm, rwb, lb, lcb, cb, rcb, rb, gk:** ya que decidimos solo quedarnos con la variable "Posicion" que representa la posicion real del jugador.
*   **player_face_url,	club_logo_url,	club_flag_url,	nation_logo_url,	nation_flag_url:** Urls que no suman informacion adicional para el análisis.
"""

df = df[['short_name', 'player_positions','overall', 'potential','pace', 'shooting',
       'passing', 'dribbling', 'defending', 'physic', 'attacking_crossing',
       'attacking_finishing', 'attacking_heading_accuracy',
       'attacking_short_passing', 'attacking_volleys', 'skill_dribbling',
       'skill_curve', 'skill_fk_accuracy', 'skill_long_passing',
       'skill_ball_control', 'movement_acceleration', 'movement_sprint_speed',
       'movement_agility', 'movement_reactions', 'movement_balance',
       'power_shot_power', 'power_jumping', 'power_stamina', 'power_strength',
       'power_long_shots', 'mentality_aggression', 'mentality_interceptions',
       'mentality_positioning', 'mentality_vision', 'mentality_penalties',
       'mentality_composure', 'defending_marking_awareness',
       'defending_standing_tackle', 'defending_sliding_tackle',
       'goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking',
       'goalkeeping_positioning', 'goalkeeping_reflexes', 'goalkeeping_speed']]

print('Cantidad de variables de interes: ', len(df.columns))
print('-------------------------------------------------------------------------')
df.head()

df.isnull().sum()

"""**IMPUTAMOS VALORES FALTANTES**

**Reemplazo los valores nulos usando la estrategia: "most_frequent"**
"""

imputer_cols = ['pace','shooting', 'passing', 'dribbling', 'defending', 'physic', 'goalkeeping_speed']
imputer = SimpleImputer(strategy="most_frequent")
df[imputer_cols] = imputer.fit_transform(df[imputer_cols])

df.isnull().sum()

print('Cantidad de datos (filas):' , len(df))

"""**En la variable 'Player_positions' se listan todas las posiciones en la que el jugador se desarrolla, por lo cual para la finalidad de este análisis decidimos solo quedarnos con la primera**

"""

df['position'] = df['player_positions'].apply(lambda x: x.split(',')[0])
df

var_cat = df[['short_name', 'position']] # guardo las variables categoricas

df_num = df.drop(['short_name', 'player_positions', 'position' ], axis = 1) # elimino las variables categoricas
df_num.head(5)

"""**ESCALAMOS LAS VARIABLES NUMERICAS**


"""

scaler = MinMaxScaler(feature_range=(0, 1), copy=True, clip=False)
x = df_num.copy(deep=True)
x_scaled = scaler.fit_transform(x)
x_norm = pd.DataFrame(x_scaled, columns=x.columns)
x_norm.head()

"""#3) Evaluación visual e intuitiva de a dos variables por vez"""

#Agrupamiento por position
FF=['RF', 'ST', 'LW', 'LF', 'RW','CF']
MM=['CAM','CDM','CM','RM','LM']
BB=['CB','LB','RB','RWB','LWB']
GK=['GK']
def group_position(x):
    if x in FF:
        return 'FF'
    if x in MM:
        return 'MM'
    if x in BB:
        return 'BB'
    if x in GK:
        return 'GK'                
    if x is None:
        return 'S/D'

graficar = x_norm.copy(deep=True)
graficar['g_position'] = df['position'].apply(group_position)

unique = graficar['g_position'].unique()
palette = dict(zip(unique, sns.color_palette(n_colors=len(unique))))
columnas = x_norm.columns
n_cols = 4
n_rows = int((len(columnas) + 1) // n_cols) + (len(columnas) % n_cols > 0)
x = 0
for i, col in enumerate(columnas):
    subplot = 0
    fig = plt.figure(figsize=(50, 100))
    for x in range(i,len(columnas)):
        subplot = subplot + 1
        ax = fig.add_subplot(n_rows, n_cols, subplot)
        ax.set_title(columnas[x] + ' vs.' + col)
        if x == i:
            sns.kdeplot(data=graficar, x=columnas[i], fill=True)#, hue='')
        else:
            sns.scatterplot(data=graficar.sample(500), x=columnas[i], y=columnas[x], hue='g_position',palette=palette)
    print(col)
    fig.subplots_adjust(left=0, right=0.5, hspace=0.15, wspace=0.15)
    plt.show()   
    plt.close()

"""**Hay un grupo de jugadores que se diferencia con facilidad, el mismo corresponde a los Arqueros (GK).
Para el resto de posiciones, y solo a partir del análisis de los gráficos, en general se puede ver que no son claramente identificables grupos distantes unos de otros.**

## PCA

**REALIZAMOS PCA (Análisis de Componentes Principales)** 

Para Reducir el numero de variables en N componentes principales
"""

pca = PCA(n_components = 2) #se reduce a 2 columnas
reduced = pd.DataFrame(pca.fit_transform(x_norm))
reduced_kmeans = reduced.copy()
reduced_shift = reduced.copy()
reduced_jerarquico = reduced.copy()
reduced_gaus = reduced.copy()
print (pca.explained_variance_ratio_)
reduced.head()

"""#4) Uso de dos técnicas de clustering: por ejemplo k-medias, DBSCAN, mezcla de Gaussianas y/o alguna jerárquica. Elección justificada de hiper-parámetros

Utilizamos el [motodo del codo](https://www.scikit-yb.org/en/latest/api/cluster/elbow.html) (el punto de inflexión en la curva) para calcular la cantidad óptima de clusters y la funcion kneedLocator para localizarlo correctamente
"""

!pip install --upgrade kneed

from kneed import KneeLocator

scores = [KMeans(n_clusters=i).fit(reduced).inertia_ for i in range(2,12)]
kn = KneeLocator(list(range(2,12)), scores, S=1.0, curve='convex', direction='decreasing')

plt.figure(figsize=(6,5))
plt.plot(np.arange(2, 12), scores, 'bx-')
plt.xlabel('Number of clusters')
plt.ylabel("Inertia")
plt.title("Inertia of k-Means versus number of clusters")
plt.vlines(kn.knee, plt.ylim()[0], plt.ylim()[1], linestyles='dashed')

"""**Donde podemos visualizar claramente que el punto de inflexión en la curva se da para un Numero de cluster = 4**

##K-medias
"""

km = KMeans(n_clusters=4, n_init=25, random_state=0)
km = km.fit(reduced_kmeans)

# Etiquetas asignadas por el algoritmo
clusters = km.labels_

"""Parámetros seleccionados:
* n_clusters:  se utilizó la cantidad de clusters obtenidos con el Método del Codo.

* init: estrategia para asignar los centroides iniciales. Dejamos la estrategia por defecto 'k-means++', ya que la cantidad de datos no es muy grande.

* n_init: determina el número de veces que se va a repetir el proceso, utilizamos un valor alto, para no obtener resultados malos debido a una iniciación poco afortunada del proceso.
* random_state: semilla para garantizar la reproducibilidad de los resultados.
max_iter: número máximo de iteraciones permitidas.

"""

reduced_kmeans['cluster'] = clusters
reduced_kmeans['name'] = var_cat.short_name
reduced_kmeans['position'] = var_cat.position
reduced_kmeans.columns = ['x', 'y', 'cluster', 'name', 'position']
reduced_kmeans.head(10)

"""**Para lograr una mejor visualizacion de las Posiciones de cada jugador se proceden a agrupar las mismas en 3 categorias**"""

forwards=['RF', 'ST', 'LW', 'LF', 'RS', 'LS', 'RM', 'LM','RW']
midfielders=['RCM','LCM','LDM','LAM','RDM','CM','RAM','CF', 'CAM', 'CDM']
defenders=['RCB','CB','LCB','LB','RB','RWB','LWB']
goalkeepers=['GK']

def pos2(position):
    if position in forwards:
        return 'Delantero'
    
    elif position in midfielders:
        return 'Mediocampista'
    
    elif position in defenders:
        return 'Defensor'
    
    elif position in goalkeepers:
        return 'Arquero'
    
    else:
        return 'nan'

reduced_kmeans["Position2"]=reduced_kmeans["position"].apply(lambda x: pos2(x))
reduced_kmeans.head(10)

"""**Para lograr una mejor visualización de los Clusters en el grafico y lograr distinguir las posiciones agrupadas en cada uno, decidimos tomar una muestra aleatoria del DataFrame**"""

df_reducido = reduced_kmeans.sample(n = 200)

sns.set(style="white")

ax = sns.lmplot(x="x", y="y", hue='cluster', data = df_reducido, legend=False,
                   fit_reg=False, size = 10, scatter_kws={"s": 250})

texts = []
for x, y,s in zip(df_reducido.x, df_reducido.y, df_reducido.Position2):
    texts.append(plt.text(x, y,s))

ax.set(ylim=(-2, 2))
plt.tick_params(labelsize=15)
plt.xlabel("PC 1", fontsize = 20)
plt.ylabel("PC 2", fontsize = 20)

plt.show()

"""**Donde podemos observar como se forman los grupos segun las posiciones de los jugadores**"""

#Tabla de contingencia
round(pd.crosstab(reduced_kmeans.cluster,reduced_kmeans.Position2,margins=True),2)

"""##Mean-Shift"""

from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets import make_blobs

centers = [[1, 1], [-1, -1], [1, -1]]
X, _ = make_blobs(n_samples=10000, centers=centers, cluster_std=0.6)
bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500) #el ancho de banda se estima automaticamente

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)

ms.fit(reduced_shift)

clusters2 = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(clusters2)
n_clusters_ = len(labels_unique)

print("Cantidad de clusters encontrados por Mean Shift : %d" % n_clusters_)

reduced_shift['cluster'] = clusters2
reduced_shift['name'] = var_cat.short_name
reduced_shift['position'] = var_cat.position
reduced_shift.columns = ['x', 'y', 'cluster', 'name', 'position']
reduced_shift

reduced_shift["Position2"]=reduced_shift["position"].apply(lambda x: pos2(x))
reduced_shift.head(10)

#De igual manera que con el algoritmo anterior, reduzco la cantidad de datos
df_reducido = reduced_shift.sample(n=200)

sns.set(style="white")

ax = sns.lmplot(x="x", y="y", hue='cluster', data = df_reducido, legend=False,
                   fit_reg=False, size = 10, scatter_kws={"s": 250})

texts = []
for x, y,s in zip(df_reducido.x, df_reducido.y, df_reducido.Position2):
    texts.append(plt.text(x, y,s))

ax.set(ylim=(-2, 2))
plt.tick_params(labelsize=15)
plt.xlabel("PC 1", fontsize = 20)
plt.ylabel("PC 2", fontsize = 20)

plt.show()

"""**Este algoritmo solo logra agrupar los datos en 2 clusters, diferenciando los arqueros del resto de las posiciones. Incluso con la estimación automática del ancho de banda.**"""

#Tabla de contingencia
round(pd.crosstab(reduced_shift.cluster,reduced_shift.Position2,margins=True),2)

"""##Mezcla de gaussianas"""

gm = GaussianMixture(n_components=3, random_state=0)
gm.fit(reduced_gaus)
reduced_gaus = reduced_gaus.copy(deep=True)

reduced_gaus['cluster'] = gm.predict(reduced_gaus)
reduced_gaus['name'] = var_cat.short_name
reduced_gaus['position'] = var_cat.position
reduced_gaus.columns = ['x', 'y', 'cluster', 'name', 'position']
reduced_gaus.head()

reduced_gaus["Position2"]=reduced_gaus["position"].apply(lambda x: pos2(x))
reduced_gaus.head()

#Obtener los parámetros del modelo
gm.get_params()

#De igual manera que con el algoritmo anterior, reduzco la cantidad de datos
df_reducido = reduced_gaus.sample(n=200)

sns.set(style="white")

ax = sns.lmplot(x="x", y="y", hue='cluster', data = df_reducido, legend=False,
                   fit_reg=False, size = 10, scatter_kws={"s": 250})

texts = []
for x, y,s in zip(df_reducido.x, df_reducido.y, df_reducido.Position2):
    texts.append(plt.text(x, y,s))

ax.set(ylim=(-2, 2))
plt.tick_params(labelsize=15)
plt.xlabel("PC 1", fontsize = 20)
plt.ylabel("PC 2", fontsize = 20)

plt.show()

#Tabla de contingencia
round(pd.crosstab(reduced_gaus.cluster,reduced_gaus.Position2,margins=True),2)

"""**Este algoritmo clasifica mejor a los Mediocampistas, pero levemente peor a los Defensores y Delanteros.**

#5) Evaluación y Análisis de los clusters encontrados

Comparando los algoritmos utilizados, concluimos que el que mejor comportamiento tiene porcentualmente es el K-Means, ya que si bien la Mezcla de Gaussianas clasifica de mejor manera a los Mediocampistas, esta empeora la calificación de Defensores y Delanteros. Ambos clasifican muy bien a los Arqueros.

#6) Se realizó alguna normalización o escalado de la base? ¿Por qué ?

Si, se decidieron normalizar las variables numéricas utilizando el estimador "MinMaxScaler" llevando cada característica individualmente al rango comprendido entre 0-1 donde tenemos la mayor precisión.

#7) Uso de alguna transformación (proyección, Embedding) para visualizar los resultados y/o usarla como preprocesado para aplicar alguna técnica de clustering.

Se utilizo Análisis de componentes principales PCA para reducir la dimensión de la cantidad de variables y con esto seleccionar las componentes que mejor representen los datos y explican la mayor proporción de varianza para lograr un mejor agrupamiento por los distintos algoritmos.
"""