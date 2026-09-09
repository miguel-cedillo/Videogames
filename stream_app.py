import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats as st_scipy

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(
    page_title="Dashboard de Ventas de Videojuegos",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Dashboard Interactivo: Análisis de Mercado de Videojuegos")
st.markdown("""
Bienvenido al panel de análisis de ventas globales de videojuegos. 
Aquí podrás explorar las tendencias históricas, el ciclo de vida de consolas, análisis de correlación y perfiles regionales.
""")

# ==========================================
# 2. CARGA Y PREPARACIÓN DE DATOS (CON CACHÉ)
# ==========================================
@st.cache_data
def load_data():
    # En un entorno real se cargaría el archivo:
    # df = pd.read_csv('dataset/games.csv')
    
    # Para fines demostrativos con los datos de ejemplo:
    data = """Name,Platform,Year_of_Release,Genre,NA_sales,EU_sales,JP_sales,Other_sales,Critic_Score,User_Score,Rating
Wii Sports,Wii,2006.0,Sports,41.36,28.96,3.77,8.45,76.0,8,E
Super Mario Bros.,NES,1985.0,Platform,29.08,3.58,6.81,0.77,,,
Mario Kart Wii,Wii,2008.0,Racing,15.68,12.76,3.79,3.29,82.0,8.3,E
Wii Sports Resort,Wii,2009.0,Sports,15.61,10.93,3.28,2.95,80.0,8,E
Pokemon Red/Pokemon Blue,GB,1996.0,Role-Playing,11.27,8.89,10.22,1.0,,,
Tetris,GB,1989.0,Puzzle,23.2,2.26,4.22,0.58,,,
New Super Mario Bros.,DS,2006.0,Platform,11.28,9.14,6.5,2.88,89.0,8.5,E
Wii Play,Wii,2006.0,Misc,13.96,9.18,2.93,2.84,58.0,6.6,E
New Super Mario Bros. Wii,Wii,2009.0,Platform,14.44,6.94,4.7,2.24,87.0,8.4,E
Duck Hunt,NES,1984.0,Shooter,26.93,0.63,0.28,0.47,,,
Nintendogs,DS,2005.0,Simulation,9.05,10.95,1.93,2.74,,,
Mario Kart DS,DS,2005.0,Racing,9.71,7.47,4.13,1.9,91.0,8.6,E
Pokemon Gold/Pokemon Silver,GB,1999.0,Role-Playing,9.0,6.18,7.2,0.71,,,
Wii Fit,Wii,2007.0,Sports,8.92,8.03,3.6,2.15,80.0,7.7,E
Kinect Adventures!,X360,2010.0,Misc,15.0,4.89,0.24,1.69,61.0,6.3,E
Wii Fit Plus,Wii,2009.0,Sports,9.01,8.49,2.53,1.77,80.0,7.4,E
Grand Theft Auto V,PS3,2013.0,Action,7.02,9.09,0.98,3.96,97.0,8.2,M
Grand Theft Auto: San Andreas,PS2,2004.0,Action,9.43,0.4,0.41,10.57,95.0,9,M
Super Mario World,SNES,1990.0,Platform,12.78,3.75,3.54,0.55,,,
"""
    from io import StringIO
    df = pd.read_csv('dataset/games.csv')

    # Limpieza básica
    df.columns = df.columns.str.lower()
    
    # Estandarización de columnas tipo texto
    for col in ['name', 'platform', 'genre']:
        df[col] = df[col].astype(str).str.strip().str.lower()
        
    # Tratamiento de valores nulos
    df = df.dropna(subset=['year_of_release'])
    df['year_of_release'] = df['year_of_release'].astype(int)
    
    df['user_score'] = df['user_score'].replace('tbd', np.nan)
    df['user_score'] = df['user_score'].astype(float)
    df['rating'] = df['rating'].fillna('unknown')
    
    # Columna de ventas totales
    region_cols = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales']
    df['total_sales'] = df[region_cols].sum(axis=1)
    
    return df

df = load_data()

# DataFrame para datos a partir de 2010
df_2010 = df[df['year_of_release'] >= 2010].copy()

# ==========================================
# 3. PANELES Y NAVEGACIÓN EN STREAMLIT
# ==========================================
st.sidebar.header("🕹️ Menú de Navegación")
opcion = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "📋 Vista Previa y Resumen",
        "📈 Lanzamientos e Historia",
        "🎯 Ventas por Plataforma y Género",
        "⭐ Ventas vs Calificaciones",
        "🌍 Perfil por Región",
        "🧪 Pruebas de Hipótesis"
    ]
)

# ------------------------------------------
# SECCIÓN 1: VISTA PREVIA
# ------------------------------------------
if opcion == "📋 Vista Previa y Resumen":
    st.header("📋 Vistazo General al Conjunto de Datos")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Juegos", f"{len(df):,}")
    col2.metric("Ventas Globales Total", f"${df['total_sales'].sum():,.2f} M USD")
    col3.metric("Plataformas Únicas", df['platform'].nunique())
    col4.metric("Géneros Únicos", df['genre'].nunique())
    
    st.subheader("Muestra del Dataset")
    st.dataframe(df.head(10), use_container_width=True)

# ------------------------------------------
# SECCIÓN 2: LANZAMIENTOS E HISTORIA
# ------------------------------------------
elif opcion == "📈 Lanzamientos e Historia":
    st.header("📈 Cantidad de Juegos Lanzados por Año")
    
    vg_for_year = df.groupby('year_of_release')['name'].count().reset_index()
    vg_for_year.columns = ['year_of_release', 'total_videogames']
    
    fig_year = px.bar(
        vg_for_year, 
        x='year_of_release', 
        y='total_videogames',
        title="Número Total de Juegos Lanzados por Año",
        labels={'year_of_release': 'Año de Lanzamiento', 'total_videogames': 'Cantidad de Juegos'},
        color='total_videogames',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_year, use_container_width=True)
    
    st.info("""
    **Conclusión:** Se observa un crecimiento histórico acelerado en la industria hasta alcanzar picos máximos entre 2008 y 2009. 
    Posteriormente, la producción de títulos físicos decayó y se estabilizó hacia 2012–2016.
    """)

# ------------------------------------------
# SECCIÓN 3: VENTAS POR PLATAFORMA Y GÉNERO
# ------------------------------------------
elif opcion == "🎯 Ventas por Plataforma y Género":
    st.header("🎯 Análisis de Ventas por Plataforma y Género")
    
    tab1, tab2, tab3 = st.tabs(["Top Plataformas", "Distribución (Boxplot)", "Ventas por Género"])
    
    with tab1:
        st.subheader("Evolución de Ventas Anuales por Plataforma (Líderes)")
        top_n = st.slider("Selecciona el número de top plataformas a visualizar:", 3, 10, 5)
        top_platforms = df.groupby('platform')['total_sales'].sum().nlargest(top_n).index.tolist()
        
        df_top = df[df['platform'].isin(top_platforms)]
        ventas_anuales = df_top.groupby(['year_of_release', 'platform'])['total_sales'].sum().reset_index()
        
        fig_lines = px.line(
            ventas_anuales, 
            x='year_of_release', 
            y='total_sales', 
            color='platform',
            markers=True,
            title=f"Distribución de Ventas Anuales para el Top {top_n} de Plataformas",
            labels={'year_of_release': 'Año', 'total_sales': 'Ventas (M USD)'}
        )
        st.plotly_chart(fig_lines, use_container_width=True)
        
    with tab2:
        st.subheader("Distribución de Ventas por Plataforma (A partir de 2010)")
        fig_box = px.box(
            df_2010, 
            x='platform', 
            y='total_sales',
            points=False, # Ocultar dispersión extrema similar a showfliers=False
            color='platform',
            title="Distribución de Ventas Globales por Plataforma",
            labels={'platform': 'Plataforma', 'total_sales': 'Ventas Totales (M USD)'}
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
    with tab3:
        st.subheader("Ventas Totales por Género")
        genre_sales = df_2010.groupby('genre')['total_sales'].sum().reset_index().sort_values('total_sales', ascending=False)
        fig_genre = px.bar(
            genre_sales,
            x='genre',
            y='total_sales',
            color='genre',
            title="Ventas Acumuladas por Género de Videojuego (A partir de 2010)",
            labels={'genre': 'Género', 'total_sales': 'Ventas Totales (M USD)'}
        )
        st.plotly_chart(fig_genre, use_container_width=True)

# ------------------------------------------
# SECCIÓN 4: CALIFICACIONES VS VENTAS
# ------------------------------------------
elif opcion == "⭐ Ventas vs Calificaciones":
    st.header("⭐ Relación entre Critic Score y Ventas Totales")
    
    vg_critic = df_2010.dropna(subset=['critic_score'])
    
    if len(vg_critic) > 0:
        correlacion = vg_critic['critic_score'].corr(vg_critic['total_sales'])
        st.metric("Coeficiente de Correlación de Pearson", f"{correlacion:.2f}")
        
        fig_scatter = px.scatter(
            vg_critic,
            x='critic_score',
            y='total_sales',
            trendline="ols",
            trendline_color_override="red",
            color='platform',
            hover_data=['name'],
            title="Relación Critic Score vs Ventas Totales",
            labels={'critic_score': 'Puntuación de la Crítica (0-100)', 'total_sales': 'Ventas (M USD)'}
        )
        fig_scatter.update_yaxes(range=[0, 10]) # Limitar visualmente el eje Y
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("No hay suficientes datos con evaluaciones de la crítica en este subconjunto.")

# ------------------------------------------
# SECCIÓN 5: PERFIL REGIONAL
# ------------------------------------------
elif opcion == "🌍 Perfil por Región":
    st.header("🌍 Comparativa de Mercado por Región")
    
    regiones_map = {'na_sales': 'Norteamérica', 'eu_sales': 'Europa', 'jp_sales': 'Japón', 'other_sales': 'Otros'}
    
    # Transformación de datos para gráfico por región y género
    df_region_genre = df_2010.groupby('genre')[list(regiones_map.keys())].sum().reset_index()
    df_long_genre = df_region_genre.melt(id_vars='genre', var_name='region', value_name='sales')
    df_long_genre['region'] = df_long_genre['region'].map(regiones_map)
    
    fig_region = px.bar(
        df_long_genre,
        x='region',
        y='sales',
        color='genre',
        barmode='group',
        title="Ventas por Género según la Región (M USD)",
        labels={'region': 'Región', 'sales': 'Ventas (M USD)', 'genre': 'Género'}
    )
    st.plotly_chart(fig_region, use_container_width=True)

# ------------------------------------------
# SECCIÓN 6: PRUEBAS DE HIPÓTESIS
# ------------------------------------------
elif opcion == "🧪 Pruebas de Hipótesis":
    st.header("🧪 Evaluación Estadísticas e Hipótesis")
    
    st.subheader("1. Hipótesis: Calificaciones promedio de Usuarios (Xbox One vs. PC)")
    st.write("**H0:** No existen diferencias entre las calificaciones promedio de usuarios para Xbox One y PC.")
    st.write("**H1:** Existen diferencias entre las calificaciones promedio de usuarios para Xbox One y PC.")
    
    xone_score = df_2010[df_2010['platform'] == 'xone']['user_score'].dropna()
    pc_score = df_2010[df_2010['platform'] == 'pc']['user_score'].dropna()
    
    alpha = 0.05
    
    if len(xone_score) > 1 and len(pc_score) > 1:
        _, p_levene = st_scipy.levene(xone_score, pc_score)
        equal_var_opt = False if p_levene < alpha else True
        
        results = st_scipy.ttest_ind(xone_score, pc_score, equal_var=equal_var_opt)
        
        st.write(f"- **Promedio User Score Xbox One:** {xone_score.mean():.2f}")
        st.write(f"- **Promedio User Score PC:** {pc_score.mean():.2f}")
        st.write(f"- **Valor p (p-value):** {results.pvalue:.4f}")
        
        if results.pvalue < alpha:
            st.error("Rechazamos la hipótesis nula (H0). Existe una diferencia estadísticamente significativa.")
        else:
            st.success("No podemos rechazar la hipótesis nula (H0). No hay evidencia suficiente para afirmar una diferencia.")
    else:
        st.info("Insuficientes datos en la muestra de ejemplo para calcular la Prueba t en esta categoría.")