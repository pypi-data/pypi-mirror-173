
<a target="_blank" rel="noopener noreferrer nofollow" href="https://camo.githubusercontent.com/981d48e57e23a4907cebc4eb481799b5882595ea978261f22a3e131dcd6ebee6/68747470733a2f2f70616e6461732e7079646174612e6f72672f7374617469632f696d672f70616e6461732e737667"><img src="https://camo.githubusercontent.com/981d48e57e23a4907cebc4eb481799b5882595ea978261f22a3e131dcd6ebee6/68747470733a2f2f70616e6461732e7079646174612e6f72672f7374617469632f696d672f70616e6461732e737667" data-canonical-src="https://pandas.pydata.org/static/img/pandas.svg" style="max-width: 100%;"></a><br>

<p dir="auto"><a href="https://pypi.org/project/pandas/" rel="nofollow"><img src="https://camo.githubusercontent.com/74cb3c88c43d4266705ae6ec7fddc1bbf603eb6d15bf2202ceb3416cd26b7c0d/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f70616e6461732e737667" alt="PyPI Latest Release" data-canonical-src="https://img.shields.io/pypi/v/pandas.svg" style="max-width: 100%;"></a>
 
# meteodata

## ¿Qué es?
meteodata es un paquete de Python que proporciona el acceso a datos meteorológicos para que el análisis de estos sea más rápido y sencillo. Después de definir cualquier ubicación, descarga datos metereológicos de temperatura, humedad, viento, precipitación y estado del cielo de las últimas 48 horas. Ofrece la posibilidad de mostrar los datos por pantalla como texto o por visualizaciones generando imágenes.     


## Principales características
La librería puede hacer las siguientes cosas:
* Muestra coordenadas de latitud y longitud de la ubicación introducida a través de Nominatim.
* Descarga de los datos en formato json.
* Temperatura de las últimas 48 horas en ºC.
* Humedad de las últimas 48 horas en g/m3.
* Rachas de viento de las últimas 48 horas en m/s.
* Precipitación de los últimos 48 minutos en l/m2.
* Tipos de estados de cielo.
* Posibilidad de mostrar gráficamnete los datos descargados mediante descriptivos numéricos, boxplots, gráficos de líneas y barras.

## Dónde conseguirlo
El código fuente está actualmente alojado en GitHub en: https://github.com/pandas-dev/pandas.
Los instaladores para la última versión publicada están disponibles en Python Package Index (PyPI).
<div class="highlight highlight-source-shell notranslate position-relative overflow-auto" dir="auto" data-snippet-clipboard-copy-content="# PyPI
pip install pandas"><pre><span class="pl-c"><span class="pl-c">#</span> PyPI</span>
pip install pandas</pre></div>

## Dependencias
<li><a href="https://pypi.org/project/requests/" rel="nofollow">requests - Realiza la petición de los datos a la API.</a></li>
<li><a href="https://geopy.readthedocs.io/en/stable/" rel="nofollow">geopy - Ofrece as coordenadas de la ubicación introducida a través de la API Nominatim.</a></li>
<li><a href="https://pypi.org/project/pandas/" rel="nofollow">pandas - Ofrece soporte y funciones para realizar descriptivos numéricos de los datos.</a></li>
<li><a href="https://matplotlib.org/" rel="nofollow">matplotlib - Ofrece funciones para realizar gráficos de lineas de los datos.</a></li>
<li><a href="https://seaborn.pydata.org/" rel="nofollow">seaborn - Ofrece funciones para realizar gráficos de líneas y barras de los datos.</a></li>

## Documentación
La documentación oficial está alojada en PyData.org: https://pandas.pydata.org/pandas-docs/stable
