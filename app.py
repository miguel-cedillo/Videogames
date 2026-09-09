
#importación de librerías
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats as st


# In[2]:


# extraer el dataset y revisar los datos
videogames_df = pd.read_csv('/datasets/games.csv')
videogames_df.info()
print(videogames_df.duplicated().sum())


# Nuestro DataFrame (DF) se conforma de 16,715 entradas y 11 columnas.
# 
# Se observan valores nulos en las columnas como Name, Year_of_Relase, Genre, Critic_Score, User_Score y Rating.
# 
# Adicionalmente se observa que la columna Year_Of_Relase es de tipo float64, y se considera que debería se de tipo int, así como la columna User_Score debe ser de tipo float64.
# 
# No se encontraron filas duplicadas por el momento.

# In[3]:


#visualizar los datos de las columnas
videogames_df.head()


# Limpieza y Preparación de Datos
# 
# Estandarización de variables de texto: Homologación de las columnas de tipo texto (object), eliminando espacios en blanco al inicio y al final, y convirtiendo todo el texto a minúsculas para garantizar la consistencia del conjunto de datos.
# 
# Transformación de tipos de datos: Conversión explícita de cada columna al tipo de dato adecuado (numérico, fecha, categórico, etc.) para optimizar el procesamiento.
# 
# Tratamiento de valores ausentes: Evaluación e imputación estratégica de datos faltantes con el propósito de preservar la integridad de la muestra y evitar sesgos en los resultados finales.

# In[4]:


#limpiar los valores de las columnas de tipo object pasandolos a minúsculas y elimimando los espacios iniciales y finales en blanco
columnas = ['Name', 'Platform', 'Genre']
for col in columnas:
    videogames_df[col] = videogames_df[col].astype(str).str.strip().str.lower()
videogames_df.head(3)


# In[5]:


#cambiemos el nombre de las columnas a minúsculas
videogames_df.columns = videogames_df.columns.str.lower()
print(videogames_df.columns)


# Para decidir como vamos a trabajar con los valores nulos, vamos a visualizarlos

# In[6]:


video_games_filtered_year = videogames_df[videogames_df['year_of_release'].isna()]
video_games_filtered_year.head()


# In[7]:


videogames_df['year_of_release'].describe()


# Las 269 filas representan 1.6% del total del dataset y no pueden usarse en análisis temporales, por lo tanto se decide eliminar estas filas.

# In[8]:


# Eliminar las filas de los valores nulos de la columna year_of_release
videogames_df = videogames_df.dropna(subset=['year_of_release'])
videogames_df['year_of_release']= videogames_df['year_of_release'].astype(int)
videogames_df.info()


# In[9]:


#visualizar las filas de los valores nulos de la columna critic_score
video_games_filtered_critic_score = videogames_df[videogames_df['critic_score'].isna()]
video_games_filtered_critic_score.head()


# In[10]:


videogames_df['critic_score'].describe()


# Se ha observado que aproximadamente el 50% de los valores nulos de la columna critic_score son nulos, por lo que no es recomendable rellenar estos valores con la mediana, en este caso por el momento con imputaremos los valores en el DF original y solo se realizará individualmente cuando sea necesario utilizar la información de esa columna.

# En el siguiente paso vamos a transformar los valores TBD de la columna user_score a NaN, para posteriormente transformar toda la columna a valores de tipo float y despues rellenarlos.

# In[11]:


#Remplazar los valores'TBD' por NaN
videogames_df['user_score'] = videogames_df['user_score'].replace('tbd', np.nan)
videogames_df['user_score']= videogames_df['user_score'].astype(float)
videogames_df.info()


# In[12]:


videogames_df['user_score'].describe()


# Revisemos que datos tiene la columna rating para decidir que hacer con los valores nulos.

# In[13]:


#visualizar las filas de los valores nulos de la columna rating
filtered_nan_rating = videogames_df[videogames_df['rating'].isna()]
filtered_nan_rating.head(10)


# Se puede deducir que los valores nulos de la columna rating corresponden a juegos no clasificados y al ser del tipo object solo los rellenaremos con el valor unknown.

# In[14]:


videogames_df['rating'] = videogames_df['rating'].fillna('unknown')
videogames_df.info()
videogames_df.duplicated().sum()


# Ya no existen valores nulos en la columna rating y no se observan filas dupicadas en el DF.

# Como paso final en la preparación del conjunto de datos, se incorporará al dataframe una variable adicional que calcule las ventas totales sumando todas las regiones.

# In[15]:


#Vamos a crear la columna de ventas totales
columnas_a_sumar= ['na_sales', 'eu_sales', 'jp_sales', 'other_sales']
videogames_df['total_sales'] = videogames_df[columnas_a_sumar].sum(axis=1)
videogames_df.head(3)


# In[16]:


#Vamos a agrupar el número de juegos lanzados por año
vg_for_year = videogames_df.groupby('year_of_release')['name'].count().reset_index()
vg_for_year.columns=['year_of_release', 'total_videogames']
print(vg_for_year)



# In[17]:


#crear gráfica para visualizar el comportamiento del número de juegos lanzados por año.
sns.barplot(data=vg_for_year, x='year_of_release', y='total_videogames', palette='viridis')

# Personalización
plt.title('Número Total de Juegos Lanzados por Año', fontsize=14, fontweight='bold')
plt.xlabel('Año de Lanzamiento', fontsize=12)
plt.ylabel('Cantidad de Juegos', fontsize=12)
plt.xticks(rotation=90)  # Rotar 90 grados para leer claramente cada año

plt.tight_layout()
plt.show()


# Entre 1980 y 1994, la industria de los videojuegos mantuvo un crecimiento moderado. A partir de 1995, se observa una aceleración sostenida en la producción de títulos hasta alcanzar su pico histórico en 2008, año en el que se lanzaron 1,427 videojuegos manteniendose casi la misma cantidad en 2009. Posterior a este hito, la cantidad de estrenos experimentó un descenso drástico, registrando únicamente 502 títulos en 2016, lo que representa una reducción del 65% respecto al punto máximo (un 35.17% del volumen alcanzado en 2008).
# Sin embargo del año 2012 a 2016 se estabilizó la baja manteniendo un número de juegos lanzados en un rango entre 502 a 653. Teniendo en cuenta esta referencia se estima que para el año 2017 se lance una cantidad de juegos entre 450 a 550 juegos.

# Analisis para observar como varían las ventas de una plataforma a otra.

# In[18]:


#Vamos a agrupar el DF por la columna platform y sumar las ventas totales
platform_sales = videogames_df.groupby('platform')['total_sales'].sum().reset_index()
platform_sales.columns=['platform', 'total_sales']
print(platform_sales.sort_values('total_sales').reset_index())


# In[19]:


platform_sales['total_sales'].describe()


# Una vez que visualizamos las ventas totales de las plataformas nos damos cuenta que existen muchas plataformas con ventas muy por debajo de la media y la mediana, por lo que se considera solo trabajar con las 10 plaformas que tienen mayores ventas.

# In[20]:


#crear un DF con el top de las plataformas

top_n = 10 #elegir el top con el que rqueremos trabajar
top_platforms = videogames_df.groupby('platform')['total_sales'].sum().nlargest(top_n).index.tolist()
print("Las plataformas líderes son:", top_platforms)
df_top = videogames_df[videogames_df['platform'].isin(top_platforms)]


# Agrupar ventas por año y plataforma (top 10)

# In[21]:


# Crear una tabla dinámica (pivot table) con los años en filas y plataformas en columnas
ventas_anuales = df_top.pivot_table(
    index='year_of_release', 
    columns='platform', 
    values='total_sales', 
    aggfunc='sum',
    fill_value=0
)
# Inspeccionar los primeros datos
ventas_anuales.head()


# Visualizar la distribución anual por plataforma

# In[22]:


plt.figure(figsize=(14, 6))

for platform in top_platforms:
    # Graficar solo los años donde la consola tuvo ventas > 0 para evitar líneas continuas en ceros
    datos_plataforma = ventas_anuales[platform][ventas_anuales[platform] > 0]
    plt.plot(datos_plataforma.index, datos_plataforma.values, marker='o', linewidth=2, label=platform)

plt.title('Distribución de Ventas Anuales por Plataforma Líder', fontsize=14, fontweight='bold')
plt.xlabel('Año de Lanzamiento', fontsize=12)
plt.ylabel('Ventas Totales (Millones USD)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Plataforma', fontsize=11)

# Ajustar las marcas del eje X
plt.xticks(range(int(df_top['year_of_release'].min()), int(df_top['year_of_release'].max()) + 1, 2), rotation=45)

plt.tight_layout()
plt.show()


# La gráfica evidencia que la mayoría de las plataformas líderes en ventas surgieron a partir del año 2000. Un hallazgo relevante es que el ciclo de vida comercial de una consola oscila entre los 5 y 7 años: alcanzan su punto máximo de ventas a los pocos años de su lanzamiento y, posteriormente, sufren una contracción abrupta a medida que ingresan nuevas plataformas al mercado.
# 
# Hacia 2016, se observa una tendencia general a la baja en las ventas totales, explicada por la escasa introducción de plataformas exitosas desde 2013.
# 
# Las plataformas que se consideraban como exitosas anteriormente como el caso de ds, xbox360, ps 3 y wii están por desaparecer del mercado.

# In[23]:


df_top['year_of_release'].describe()


# Con base en los datos observados anteriormente utilizaremos los datos de las plataformas que hayan lanzado juegos en 2010 hasta la fecha para hacer una proyección del éxito en el mercado de los videojuegos para el año 2017.

# Vamos a crear un DF con los datos de las plataformas lanzadas a partir del año 2010.

# In[24]:


videogames_release_2010 = videogames_df[videogames_df['year_of_release']>= 2010].reset_index()
videogames_release_2010.head(3)


# In[25]:


videogames_release_2010.info()


# In[26]:


#visualizar solo los valores únicos de la columna platform
print(videogames_release_2010['platform'].unique())
#visualizar solo los valores únicos de la columna year_of_release
print(videogames_release_2010['year_of_release'].unique())


# In[27]:


# Crear una tabla dinámica (pivot table) con los años en filas y plataformas en columnas
ventas_anuales_2010 = videogames_release_2010.pivot_table(
    index='year_of_release', 
    columns='platform', 
    values='total_sales', 
    aggfunc='sum',
    fill_value=0
)
# Inspeccionar los datos
ventas_anuales_2010.head(8)


# In[28]:


plt.figure(figsize=(14, 6))

for platform in ventas_anuales_2010:
    # Graficar solo los años donde la consola tuvo ventas > 0 para evitar líneas continuas en ceros
    datos_plataforma = ventas_anuales_2010[platform][ventas_anuales_2010[platform] > 0]
    plt.plot(datos_plataforma.index, datos_plataforma.values, marker='o', linewidth=2, label=platform)

plt.title('Distribución de Ventas Anuales por Plataforma Líder con Ventas a PArtir 2010', fontsize=14, fontweight='bold')
plt.xlabel('Año de Lanzamiento', fontsize=12)
plt.ylabel('Ventas Totales (Millones USD)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Plataforma', fontsize=11)

# Ajustar las marcas del eje X
plt.xlim(2009, 2017)
plt.tight_layout()
plt.show()


# 
# El gráfico ilustra la distribución de las ventas de videojuegos durante el periodo 2010–2016, evidenciando un claro relevo generacional en la industria:Declive de la séptima generación: En 2010, el mercado estaba dominado por Xbox 360 (con más de 170 millones USD), PlayStation 3 (150 millones USD) y Wii (más de 125 millones USD). Sin embargo, para 2016 las tres plataformas registraron ventas inferiores a los 10 millones USD, marcando la fase final de su ciclo de vida comercial.
# Liderazgo de la octava generación: Para 2016, el mercado pasó a ser liderado por PlayStation 4 (70 millones USD) y Xbox One (25 millones USD), aunque ambas cifras se sitúan ya por debajo de sus respectivos picos históricos.
# Conclusión prospectiva: La tendencia general indica una contracción sostenida en las ventas para 2017 a lo largo de todas las plataformas, anticipando un panorama complejo para la comercialización global de videojuegos.

# In[29]:


# 1. Crear el boxplot
sns.boxplot(
    data=videogames_release_2010, 
    x='platform', 
    y='total_sales', 
    palette='Set2',
    showfliers=False  # Pon False si deseas ocultar los puntos atípicos
        )

# 2. Personalización del gráfico
plt.title('Distribución de Ventas Globales por Plataforma', fontsize=14, fontweight='bold')
plt.xlabel('Plataforma', fontsize=12)
plt.ylabel('Ventas Totales (Millones USD)', fontsize=12)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# 
# El análisis mediante boxplot revela que las plataformas Xbox 360, PS3, PS4 y Xbox One registran los picos de ventas más elevados, superando el umbral de los 150 millones de USD. La mayoría de las distribuciones presenta un sesgo positivo, lo que indica una concentración de los datos en valores bajos con extensas colas hacia ventas altas. Aunque los valores atípicos (outliers) fueron omitidos de la visualización, la longitud de los bigotes superiores confirma la presencia recurrente de títulos o periodos con ingresos atípicamente altos.
# 
# En contraste, consolas como PSP, PS Vita y PS2 se encuentran en la fase final de su ciclo comercial, como lo demuestra una mediana de ventas totales muy próxima a cero.

# Correlación de ventas totales de la plataforma PS4 y la calificación de la crítica:

# In[30]:


df_ps4 = videogames_release_2010[videogames_release_2010['platform']== 'ps4'] #filtrar el DF por plataforma X360
#eliminar valores nulos de la columna critic_score
df_ps4 = df_ps4.dropna(subset=['critic_score'])
# Calcular la correlación entre ambas columnas
correlacion_ps4 = df_ps4['critic_score'].corr(df_ps4['total_sales'])
print(f"Correlación entre la puntuación de la crítica y las ventas totales: {correlacion_ps4:.2f}")


# In[31]:


#Eliminar los valores nulos de la columna critic_score
vg_critic = videogames_release_2010.dropna(subset=['critic_score'])
# Calcular la correlación entre ambas columnas
videogames_corr = vg_critic['critic_score'].corr(vg_critic['total_sales'])
print(f"Correlación entre la puntuación de la crítica y las ventas totales: {videogames_corr:.2f}")


# In[32]:


# Configurar estilo
sns.set_style('whitegrid')

# Crear gráfico de dispersión con línea de regresión
g = sns.regplot(
    data=vg_critic, 
    x='critic_score', 
    y='total_sales', 
    scatter_kws={'alpha':0.3, 'color':'#1f77b4'}, # Puntos semi-transparentes
    line_kws={'color':'red'} # Línea de tendencia roja
)

# Personalización
plt.title(f'Relación Critic Score - Ventas\n(Correlación: {videogames_corr:.2f})', fontsize=13, fontweight='bold')
plt.xlabel('Puntuación de la Crítica (0-100)', fontsize=11)
plt.ylabel('Ventas Totales (Millones USD)', fontsize=11)

# --- IMPORTANTE: Ajustar zoom para enfocar la mayoría de datos ---
plt.ylim(0, 10) # Enfocarse en juegos que vendieron entre 0 y 5 millones
plt.xlim(20, 100) # Omitir puntuaciones extremadamente bajas si hay pocas

plt.show()


# El análisis muestra una correlación positiva débil (r = 0.32) entre las calificaciones de la crítica y el volumen de ventas globales. Si bien una puntuación alta por parte de los especialistas no garantiza el éxito comercial de un título, se observa un patrón claro en el extremo opuesto: ningún videojuego con calificaciones bajas logró superar el umbral de los 5 millones de USD en ventas.
# 
# En conclusión, una recepción crítica desfavorable actúa como un límite para el desempeño comercial del juego, mientras que una evaluación sobresaliente es una condición favorable, pero no suficiente por sí sola, para asegurar altas ventas.
# 

# Vamos a hacer un análisis de las ventas de los videojuegos en sus diferentes plataformas.

# Primer paso filtrar los videojuegos que hayan salido en más de una plataforma

# In[33]:


#Filtrar solo juegos que hayan salido en más de 1 plataforma
juegos_multi = videogames_release_2010.groupby('name').filter(lambda x: x['platform'].nunique() > 1)
print(juegos_multi['name'].unique()) #visualizar los juegos multiplataforma
print(juegos_multi['name'].nunique()) #contar los juegos multiplataforma

# 2. Seleccionar los Top 10 juegos multiplataforma por ventas acumuladas
top_10_juegos = (
    juegos_multi.groupby('name')['total_sales']
    .sum()
    .nlargest(10)
    .index
)

# 3. Crear el DataFrame filtrado
df_comparativa = videogames_release_2010[videogames_release_2010['name'].isin(top_10_juegos)]


# Vamos a hacer un gráfico de barras para observar el comportamiento de las ventas del videojuego por cada plataforma.

# In[34]:


ax = sns.barplot(
    data=df_comparativa,
    x='name',
    y='total_sales',
    hue='platform',
    palette='tab10'
)

# Personalización
plt.title('Comparativa de Ventas por Plataforma para el Mismo Juego', fontsize=14, fontweight='bold')
plt.xlabel('Título del Juego', fontsize=12)
plt.ylabel('Ventas Totales (Millones USD)', fontsize=12)
plt.xticks(rotation=45, ha='right')

# Colocar la leyenda de plataformas fuera del gráfico para evitar superposición
plt.legend(title='Plataforma', bbox_to_anchor=(1.02, 1), loc='upper left')

plt.tight_layout()
plt.show()


# Vamos a crear un mapa de calor también.

# In[35]:


# Crear tabla dinámica: Filas = Juegos, Columnas = Plataformas, Valores = Ventas
tabla_pivot = df_comparativa.pivot_table(
    index='name',
    columns='platform',
    values='total_sales',
    aggfunc='sum',
    fill_value=0  # Rellenar con 0 si el juego no salió en esa plataforma
)

plt.figure(figsize=(11, 7))

# Crear heatmap con anotaciones numéricas
sns.heatmap(
    tabla_pivot, 
    annot=True, 
    fmt=".2f", 
    cmap='YlGnBu', 
    cbar_kws={'label': 'Ventas (Millones USD)'}
)

plt.title('Matriz de Ventas: Juego vs Plataforma', fontsize=14, fontweight='bold')
plt.xlabel('Plataforma', fontsize=12)
plt.ylabel('Título del Juego', fontsize=12)

plt.tight_layout()
plt.show()


# En ambos gráficos se puede observar que las plataformas preferidas para jugar son PS3 y X360.

# Análisis de la venta de videojuegos por género

# In[36]:


#crear un DF agrupado por género
genre_sales= videogames_release_2010.groupby('genre')['total_sales'].sum().reset_index()
genre_sales.head()


# In[37]:


#gráfico de barras
genre_sales.plot(x= 'genre', y='total_sales', kind = 'bar', ylabel= 'Ventas Totales (Millones USD)', xlabel= 'Género de videojuego', legend= False, title= 'Ventas por Género'
)


# El género de Acción es el más vendido con más de 600 millones de USD, le siguen shooter y sports, y los juegos de puzzle y strategy son los menos vendidos.

# Paso 4: Perfil de Usuario para cada Región

# In[38]:


#top 5 de plataformas con más ventas
top_5 =5
top_5_platforms = videogames_df.groupby("platform")["total_sales"].sum().nlargest(top_5).index.tolist()
df_top_5 = videogames_df[videogames_df["platform"].isin(top_5_platforms)]

print("Las plataformas top 10 son:", top_5_platforms)


# In[39]:


#1. Definir las columnas regionales de ventas
region_cols = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales']
# 2. Agrupar las ventas por plataforma en cada región
ventas_regionales = videogames_release_2010.groupby('platform')[region_cols].sum()
# 3. Filtrar para incluir solo las plataformas con ventas significativas (ej. Top 8 globales)
ventas_regionales = ventas_regionales.loc[top_5_platforms]
# 4. Convertir las ventas absolutas a porcentajes (cuotas de mercado) por región
# Dividimos cada columna entre su suma total para que la región sume 100%
cuotas_mercado = ventas_regionales.div(ventas_regionales.sum(axis=0), axis=1) * 100

print(cuotas_mercado.round(2))


# Gráfico de barras agrupadas

# In[40]:


# Transformar la tabla de cuotas a formato largo para poder graficarlo
cuotas_long = cuotas_mercado.reset_index().melt(
    id_vars='platform', 
    var_name='region', 
    value_name='market_share'
)
print(cuotas_long.round(2))


# In[41]:


# Convertir de formato largo a formato ancho para apilar
cuotas_pivot = cuotas_long.pivot(index='region', columns='platform', values='market_share')

# Graficar barras apiladas
ax = cuotas_pivot.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab10')

plt.title('Cuota de Mercado Acumulada por Región (%)', fontsize=14, fontweight='bold')
plt.xlabel('Región', fontsize=12)
plt.ylabel('Cuota de Mercado (%)', fontsize=12)
plt.xticks(rotation=0)  # Mantiene los nombres de las regiones horizontales
plt.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()


# In[42]:


# Diccionario para mapear nombres de columnas a etiquetas claras
regiones = {
    'na_sales': 'Norteamérica',
    'eu_sales': 'Europa',
    'jp_sales': 'Japón',
    'other_sales': 'Otros'
}

def perfil_regional(df, columna_interes, top_n=5):
    """
    Calcula las ventas absolutas y la cuota de mercado (%) 
    para las N principales categorías por región.
    """
    resultados = {}

    for col_region, nombre_region in regiones.items():
        # Ventas totales acumuladas de la categoría en esa región
        ventas = df.groupby(columna_interes)[col_region].sum().nlargest(top_n)

        # Porcentaje sobre el total de ventas de esa región
        cuota = (ventas / df[col_region].sum()) * 100

        # Consolidar en un DataFrame
        resultados[nombre_region] = pd.DataFrame({
            'Ventas (M USD)': ventas.round(2),
            'Cuota (%)': cuota.round(2)
        })

    return pd.concat(resultados, axis=1)


# In[43]:


top_plataformas = perfil_regional(videogames_release_2010, 'platform', top_n=5)
print("=== TOP 5 PLATAFORMAS POR REGIÓN ===")
display(top_plataformas)


# Vamos a módificar la tabla anterior para poder hacer una gráfica de barras.

# In[44]:


#Resetear el índice para que la categoría plataforma pase a ser una columna
df_flat = top_plataformas.reset_index()
# Aplanar las columnas multinivel a formato largo
# Un stack(level=0) pasa el primer nivel de columnas (Norteamérica, Europa, etc.) a las filas
df_long = df_flat.set_index('platform').stack(level=0).reset_index()
# Renombrar las columnas para mayor claridad
df_long.columns = ['platform', 'region', 'ventas_m_usd', 'cuota_pct']
# Eliminar filas con valores nulos (plataformas que no entraron en el Top N de esa región)
df_long = df_long.dropna(subset=['cuota_pct'])


# In[45]:


plt.figure(figsize=(12, 6))

sns.barplot(
    data=df_long,
    x='region',
    y='ventas_m_usd',
    hue='platform',
    palette='tab10'
)

plt.title('Ventas de las Principales Plataformas por Región (M USD)', fontsize=14, fontweight='bold')
plt.xlabel('Región', fontsize=12)
plt.ylabel('Ventas (Millones USD)', fontsize=12)
plt.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()



# El gráfico de barras muestra las ventas de las principales plataformas por región.
# Se observa que en Europa y Otros la plataforma lider es el PS3, en Norteamérica es X360 y y en Japón es el 3DS.

# Análisis por género

# In[46]:


#top_5_generos
top_generos = perfil_regional(videogames_release_2010, 'genre', top_n=5)
print("=== TOP 5 GÉNEROS POR REGIÓN ===")
display(top_generos)


# Vamos a restablecer la tabla anterior para poder elaborar una gráfica de barras

# In[47]:


#Resetear el índice para que la categoría género pase a ser una columna
df_flat = top_generos.reset_index()
# Aplanar las columnas multinivel a formato largo
# Un stack(level=0) pasa el primer nivel de columnas (Norteamérica, Europa, etc.) a las filas
df_long_genre = df_flat.set_index('genre').stack(level=0).reset_index()

# Renombrar las columnas para mayor claridad
df_long_genre.columns = ['genre', 'region', 'ventas_m_usd', 'cuota_pct']

# Eliminar filas con valores nulos (plataformas que no entraron en el Top N de esa región)
df_long = df_long.dropna(subset=['cuota_pct'])



# In[48]:


plt.figure(figsize=(12, 6))

sns.barplot(
    data=df_long_genre,
    x='region',
    y='ventas_m_usd',
    hue='genre',
    palette='tab10'
)

plt.title('Ventas de los Principales Géneros por Región (M USD)', fontsize=14, fontweight='bold')
plt.xlabel('Región', fontsize=12)
plt.ylabel('Ventas (Millones USD)', fontsize=12)
plt.legend(title='Género', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()



# El gráfico de barras muestra las ventas de los principales géneros por región.
# Se observa que el género de acción predomina en todas las regiones excepto en japón donde claramente lidera el género de role-playing.

# Analizar la Clasificación ESRB por Región

# In[49]:


#agrupar las ventas regionales por rating
esrb_ventas = videogames_release_2010.groupby('rating')[list(regiones.keys())].sum()
esrb_ventas.head(3)


# In[50]:


# Convertir a cuota porcentual dentro de cada región (suma columna = 100%)
esrb_cuota = esrb_ventas.div(esrb_ventas.sum(axis=0), axis=1) * 100

# Renombrar columnas para la presentación
esrb_cuota.columns = list(regiones.values())

print("=== DISTRIBUCIÓN DE VENTAS POR CLASIFICACIÓN ESRB (%) ===")
display(esrb_cuota.round(2))


# Vamos a modificar esta tabla para poder graficarla

# In[51]:


#Resetear el índice para que la categoría rating pase a ser una columna
df_flat_rating = esrb_cuota.reset_index()
# Aplanar las columnas multinivel a formato largo
# Un stack(level=0) pasa el primer nivel de columnas (Norteamérica, Europa, etc.) a las filas
df_long_rating = df_flat_rating.set_index('rating').stack(level=0).reset_index()
# Renombrar las columnas para mayor claridad
df_long_rating.columns = ['rating', 'region', 'ventas_m_usd']
# Eliminar filas con valores nulos (plataformas que no entraron en el Top N de esa región)
df_long_rating = df_long_rating.dropna(subset=['ventas_m_usd'])
df_long_rating.head()


# In[52]:


plt.figure(figsize=(12, 6))

sns.barplot(
    data=df_long_rating,
    x='region',
    y='ventas_m_usd',
    hue='rating',
    palette='tab10'
)

plt.title('Ventas de los diferentes ratings por Región (M USD)', fontsize=14, fontweight='bold')
plt.xlabel('Región', fontsize=12)
plt.ylabel('Ventas (Millones USD)', fontsize=12)
plt.legend(title='Rating', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()


# El gráfico muestra las ventas de videojuegos en millones de dólares, agrupadas por región geográfica y desglosadas por la clasificación de Edad ESRB.
# Se puede observar que el comportamiento de ventas entre Norteamérica, Europa y Otros son muy similares en todas sus categorías, con valores moderados principalmente entre 14 y 34 millones de USD, asimismo se destaca la clasificación M (Mature) como la clasificación líder en venta de estas regiones.
# Sin embargo, en Japón no se puede conocer con claridad ya que los juegos etiquetados como unknown son los que predominan.

# Perfiles por región:
# 
# •	Norteamérica (NA):
# o	Consolas: Preferencia por Xbox y PlayStation (X360, PS3/PS4, Wii).
# o	Géneros: Action y Shooter dominan con diferencia el mercado.
# o	ESRB: Fuerte presencia de juegos clasificación M (Mature) y E (Everyone).
# •	Europa (EU):
# o	Consolas: Liderazgo histórico de la marca PlayStation (PS3, PS4) con presencia de Xbox.
# o	Géneros: Action y Sports ocupan las primeras posiciones.
# o	ESRB: Distribución similar a NA, encabezada por M (Mature) y E (Everyone).
# •	Japón (JP):
# o	Consolas: Dominio casi absoluto de consolas portátiles y marcas locales (3DS, DS, PSP, PS3).
# o	Géneros: El género Role-Playing (RPG) lidera ampliamente el mercado, seguido por Action.
# o	ESRB: Gran volumen de juegos con rating Unknown (debido a que Japón usa su propio sistema de clasificación, CERO, en lugar de ESRB) y clasificación E (Everyone).
# 

# Hipótesis:

# Las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son las mismas.

# Planteamiento de Hipótesis:
# 
# H0: No existen diferencias entre las calificaciones promedio de los usuarios para las plataformas Xbox One y PC.
# 
# H1: Existen diferencias entre las calificaciones promedio de los usuarios para las plataformas Xbox One y PC.
# 
# Nivel de Significancia (alpha) =0.05

# In[55]:


#medir si las varianzas de mis grupos son iguales
xone_score = videogames_release_2010[videogames_release_2010['platform']== 'xone']['user_score'].dropna()
pc_score = videogames_release_2010[videogames_release_2010['platform']== 'pc']['user_score'].dropna()
alpha = 0.05
#conocer las varianzas
print(xone_score.var())
print(pc_score.var())

#levene si las varianzas son iguales o no, para determinar que prueba t aplicar

_,p_levene= st.levene(xone_score, pc_score)

if p_levene < alpha:
    print ('equal_var = False')
else:
    print ('equal_var = True')

#Realizar la prueba t de Student independiente
# Nota: equal_var=False aplica la prueba de Welch, recomendada cuando las varianzas o tamaños de muestra de ambos grupos pueden diferir.
results = st.ttest_ind(xone_score, pc_score, equal_var=False)

#Imprimir los resultados
print(f"Promedio User Score Xbox One: {xone_score.mean():.2f}")
print(f"Promedio User Score PC: {pc_score.mean():.2f}")
print(f"Valor p (p-value): {results.pvalue:.4f}")

#Evaluar la hipótesis
if results.pvalue < alpha:
    print("Rechazamos la hipótesis nula (H0). Existe una diferencia estadísticamente significativa entre las calificaciones de Xbox One y PC.")
else:
    print("No podemos rechazar la hipótesis nula (H0). No hay evidencia suficiente para afirmar que las calificaciones promedio sean diferentes.")



# No existe evidencia significativa para determinar que las calificaciones promedio de los usuarios para los géneros de Acción y Deportes sean diferentes.

# Planteamiento de Hipótesis:
# 
# H0: No existen diferencias entre las calificaciones promedio de los usuarios para los géneros de Acción y Deportes.
# 
# H1: Existen diferencias entre las calificaciones promedio de los usuarios para los géneros de Acción y Deportes.
# 
# Nivel de Significancia (alpha) =0.05

# In[56]:


#medir si las varianzas de mis grupos son iguales
action_score = videogames_release_2010[videogames_release_2010['genre']== 'action']['user_score'].dropna()
sports_score = videogames_release_2010[videogames_release_2010['genre']== 'sports']['user_score'].dropna()
alpha = 0.05
#conocer las varianzas
print(action_score.var())
print(sports_score.var())

#levene si las varianzas son iguales o no, para determinar que prueba t aplicar

_,p_levene= st.levene(action_score, sports_score)

if p_levene < alpha:
    print ('equal_var = False')
else:
    print ('equal_var = True')

#Realizar la prueba t de Student independiente
# Nota: equal_var=False aplica la prueba de Welch, recomendada cuando las varianzas o tamaños de muestra de ambos grupos pueden diferir.
results = st.ttest_ind(action_score, sports_score, equal_var=False)

#Imprimir los resultados
print(f"Promedio User Score Action: {action_score.mean():.2f}")
print(f"Promedio User Score Sports: {sports_score.mean():.2f}")
print(f"Valor p (p-value): {results.pvalue:.4f}")

#Evaluar la hipótesis
if results.pvalue < alpha:
    print("Rechazamos la hipótesis nula (H0). Existe una diferencia estadísticamente significativa entre las calificaciones de Action y Sports.")
else:
    print("No podemos rechazar la hipótesis nula (H0). No hay evidencia suficiente para afirmar que las calificaciones promedio sean diferentes.")



# Conclusión General

# A partir de 2011, el mercado de videojuegos experimentó una contracción significativa en sus ventas globales. Aunque durante el periodo 2012–2016 la industria mostró una estabilización en el rango de los 500 a 600 millones de USD, las proyecciones para 2017 anticipan un volumen de ingresos inferior al registrado en 2016. Este comportamiento responde principalmente al agotamiento del ciclo de vida de las consolas dominantes.
# 
# Para 2017, se prevé que PlayStation 4 y Xbox One se mantengan como las plataformas más rentables, aunque con un margen de ventas reducido respecto a años anteriores. En cuanto a la oferta de contenido, la categoría de clasificación M (Mature) se posiciona como la más lucrativa transversalmente en todas las regiones, por lo que las desarrolladoras deberían priorizar este segmento.
# 
# Finalmente, considerando la contracción generalizada del mercado mundial y la consolidación de Sony y Microsoft como los actores líderes de la industria, resulta estratégico que ambas compañías aceleren el desarrollo e introducción de hardware de nueva generación en los próximos años para reactivar la demanda global.
