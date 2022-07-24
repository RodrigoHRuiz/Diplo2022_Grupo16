## Entregable Análisis Exploratorio y Curación de Datos
## Grupo 16
- Fernanda Borghello,<br>
- Rodrigo Ruiz,<br>
- Alfonsina Szpeiner

Año 2022

## Selección de características
A partir de un análisis de correlaciones entre las variables numéricas se seleccioonaron aquellas presentaban una correlación igual o superior a 0.40 con el precio, que es la variable target.
Además, por razones didácticas se incluyeron las variables año_construccion y sup_construida.
Las variables categóricas seleccionadas fueron tales por presentar variabilidad respecto al precio de la propiedd, según sus distinto valores posibles. 
## Características seleccionadas
### Características categóricas
  Las características categóricas incluidas
  1. tipo (Type): tipo de propiedad. 3 valores posibles: h (house,cottage,villa, semi,terrace), u (unit, duplex) o t (townhouse)
  2. region (Regionname): region donde está ubicada la propiedad. 8 valores posibles.

Ambas características categóricas fueron codificadas con un método OneHotEncoding utilizando la librería scikit-learn, utulizando todos sus valores posibles.
  
### Características numéricas
  1. precio (Price): precio de venta de la propiedad en dólares australianos.
  2. habitaciones (Rooms): cantidad de habitaciones que tiene la propiedad.
  3. dormitorios (Bedroom2): número de dormitorios de la propiedad.
  3. baños (Bathroom): cantidad de baños que tiene la propiedad.
  4. cp_melb (Postcode): código postal de la propiedad.
  5. año_construccion (YearBuilt): año en que fue construida la propiedad.
  6. sup_construida (BuildingArea): superficie construida de la propiedad, en metros cu adrados.
  7. media_precio_Airbnb: Se agrega el precio promedio diario de 
     publicaciones de la plataforma AirBnB en el mismo código 
     postal (cp_melb).
  
## Limpieza:
  1. precio: se consideraron sólo a aquellos registros que se encuentraban entre los cuartiles 10 y 90 de precio.
  2. domitorios: se descarta la variable porque presenta una alta correlación (0.94) con la variable habitaciones.
  3. baños: se quitaron los registros de las propiedades que indicaban 0 en la cantidad de baños (28 registros).
  4. se descartaron los registros de los códigos postales que presentaban una frecuencia menor 108 (1% del total de los datos).

## Transformaciones:
  1. Todas las características numéricas fueron escaladas utilizando el método MinMaxScaler de la librería scikit-learn, en un intervalo de 0 a 1.
  2. Los datos faltantes de las columnas "año_construccion" y "sup_construida" fueron imputados utilizando el método de imputación multiple por ecuaciones encadenadas (MICE) con el estimador KNeighborsRegressor, de la librería scikit-learn.

## Datos aumentados
  1. Se agregaron las 2 primeras componentes principales obtenidas a través del
     método PCA de la librería scikit-lear, aplicado sobre el conjunto de datos totalmente procesado. Se seleccionaron las 2 primeras componentes que permiten explicar el 68% de la varianza de los datos.
