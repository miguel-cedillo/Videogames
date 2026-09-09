# 🎮 Video Game Sales Analytics Dashboard

¡Bienvenido al repositorio del **Dashboard Interactivo de Análisis del Mercado de Videojuegos**! Este proyecto transforma datos históricos de ventas en información estratégica mediante el desarrollo de una aplicación web interactiva.

El objetivo principal es identificar patrones de consumo, analizar la longevidad de las plataformas comerciales, medir la correlación entre la crítica y las ventas, y realizar validaciones estadísticas rigurosas para respaldar decisiones de negocio en la industria del entretenimiento digital.

> 💡 **Nota de valor:** El proyecto no solo visualiza datos, sino que automatiza la limpieza del dataset, la estandarización de variables y la ejecución de **pruebas de hipótesis t-Student** en tiempo real.

---

## 🚀 Características Principales

* 📋 **Vista Previa & KPIs:** Métricas de alto nivel (total de ventas, volumen de juegos, catálogo de plataformas) y exploración directa de los datos origen.
* 📈 **Evolución Histórica:** Análisis temporal de lanzamientos para identificar la era dorada del formato físico y tendencias de producción.
* 🎯 **Ciclo de Vida & Géneros:** Evaluación comparativa del ciclo de vida útil de consolas mediante líneas de tiempo interactivas, distribuciones (*boxplots*) y géneros líderes.
* ⭐ **Análisis de Correlación:** Estudio de dispersión con regresión OLS entre las calificaciones de la crítica (*Critic Score*) y el desempeño comercial.
* 🌍 **Perfil de Mercado Regional:** Segmentación geográfica de hábitos de consumo (Norteamérica, Europa, Japón y Resto del Mundo).
* 🧪 **Pruebas de Hipótesis:** Módulo estadístico automatizado con **Prueba de Levene** (igualdad de varianzas) y **Prueba T de Student** de muestras independientes.

---

## 🛠️ Tecnologías Utilizadas

Las herramientas seleccionadas garantizan un procesamiento de datos eficiente, análisis estadístico riguroso y una experiencia de usuario fluida:

* **Lenguaje:** ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* **Framework Web:** ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
* **Manipulación de Datos:** ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) & ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
* **Visualización Interactiva:** ![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
* **Análisis Estadístico:** ![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=white)

---

## ⚙️ Instalación y Configuración Local

Sigue estos pasos paso a paso para clonar el repositorio, configurar tu entorno virtual y ejecutar la aplicación en tu máquina local.

### Prerrequisitos

* Tener instalado **Python 3.8** o superior.
* Gestor de paquetes `pip` actualizado.

### Pasos de Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/video-games-analytics-dashboard.git
   cd video-games-analytics-dashboard
   ```

2. **Crear y activar un entorno virtual (recomendado):**
   * En Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   * En Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Instalar dependencias requeridas:**
   Asegúrate de que tus librerías estén listadas en el archivo `requirements.txt` y ejecuta:
   ```bash
   pip install -r requirements.txt
   ```

4. **Estructura de archivos esperada:**
   Verifica que la estructura de tu proyecto luzca de la siguiente forma antes de la ejecución:
   ```text
   ├── dataset/
   │   └── games.csv
   ├── app.py
   ├── requirements.txt
   └── README.md
   ```

5. **Iniciar la aplicación con Streamlit:**
   ```bash
   streamlit run app.py
   ```

6. **¡Listo!** La aplicación se abrirá automáticamente en tu navegador web predeterminado en la dirección local: `http://localhost:8501`.

---

## 📂 Estructura del Dataset

El panel procesa un dataset de la industria de videojuegos con las siguientes variables clave:

| Columna | Descripción |
| :--- | :--- |
| `name` | Nombre del videojuego |
| `platform` | Consola o plataforma de lanzamiento |
| `year_of_release` | Año de publicación |
| `genre` | Categoría o género principal |
| `na_sales`, `eu_sales`, `jp_sales`, `other_sales` | Ventas en millones de USD por región |
| `critic_score` | Puntuación otorgada por la crítica (escala 0-100) |
| `user_score` | Puntuación asignada por los usuarios (escala 0-10) |
| `rating` | Clasificación de contenido por edad (ESRB) |

---

## 🤝 Contribuciones

Las contribuciones son las que hacen de la comunidad de código abierto un lugar increíble para aprender, inspirar y crear. Cualquier contribución que hagas será **muy apreciada**.

1. Haz un *Fork* del proyecto.
2. Crea tu *Feature Branch* (`git checkout -b feature/NuevaCaracteristica`).
3. Haz *Commit* de tus cambios (`git commit -m 'Añadir NuevaCaracteristica'`).
4. Haz *Push* a la rama (`git push origin feature/NuevaCaracteristica`).
5. Abre un *Pull Request*.

---

Desarrollado con pasión para la ciencia de datos y la analítica del entretenimiento digital. 🕹️✨
