# example_package_nagore_ainhoa
Con este paquete se puede realizar un analisis descriptivo con estad�sticos y distintas visualizaciones.

Se ha seguido la siguiente estructura de carpetas y archivos:

1. Carpeta general
En esta carpeta se encuentran las siguientes carpetas y archivos.
 
  1.1. Carpeta dist
  
  1.2. Carpeta src
  En esta carpeta se encuentra la siguiente carpeta:
    
    1.2.1. Carpeta descriptive_analysis_beginners
    Dentro de esta se encuentran los siguientes 3 archivos .py

	1.2.1.1. Archivo __init__.py
	Es necesario para poder importar correctamente el directorio como un paquete, asimismo, debe estar vacio.

	1.2.1.2. Archivo functions.py
	Se encuentra la clase generada para la libreria. Cuenta con diferentes funciones para llevar a cabo el analisis exploratorio de los datos a partir de un archivo csv como input.
	- Null_Zeros, devuelve como output una tabla con las siguientes columnas; Nan values, Nan percentage (%), Zero values y Zero percentage(%). 
	- Repeated_Rows, devuelve una tabla con las filas duplicadas en caso de haberlas.
	- Repeated_Columns, devuelve una tabla con las columnas duplicadas en caso de haberlas.
	- Duplicates_UniqueValues, devuelve una tabla con los valores duplicados en caso de haberlos.
	- Numeric_Variables, con esta funcion se grafica la distribucion, devuelve descriptivos de las variables numericas.
	- Categorical_Variables, devuelve graficas para las variables categoricas.
	- Descriptives, devuelve un resumen de todas las funciones anteriores.

  1.3. Archivo LICENSE
  La licencia del paquete. Esta indica a los usuarios que instalen el paquete los terminos bajo los que pueden utilizarlo. En este caso se ha usado la licencia MIT ya que al ser de software libre permisiva pone muy pocas limitaciones en su reutilizacion y posee excelente compatibilidad de licencia. Asimismo, es compatible con muchas licencias copyleft y ni tiene copyright, lo que permite su modificacion.

  1.4. Archivo pyproject.toml
  Se divide en 3 apartados:
	
    1.4.1. Build system
    - Requires: los paquetes necesarios para instalar la libreria y poder hacer uso de ella
    - Build-backend: el nombre del objeto Python que se utilizaran para realizar la construccion.

    1.4.2. Project
    - Name: nombre del paquete
    - Version: version del paquete creado
    - Authors: autores del paquete
    - Description: breve descripcion de lo que hace este paquete
    - Readme: el archivo readme
    - Classifiers: el indice y descarga algunos metadatos adicionales sobre el paquete.

    1.4.3. Project.urls
    Se encuentran los urls tanto de github, como de bug tracker.
    This package will consist on some functions to generate a descriptive analysis.


## Pasos a seguir para usar la librer�a

! pip install descriptive-analysis-beginners==0.0.1

from descriptive_analysis_beginners import functions

eda = functions.EDA_class("ejemplo.csv")

eda.Descriptives()