import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración
st.set_page_config(page_title="Analizador Académico", layout="wide")
st.title("📚 Analizador Académico")

@st.cache_data
def cargar_datos():
    return pd.read_csv('unidos.csv')

df = cargar_datos()

# Filtros
st.sidebar.header('Filtros')
grupos = st.sidebar.multiselect(
    'Grupos:',
    options=sorted(df['grupo'].unique()),
    default=sorted(df['grupo'].unique())
)
semestres = st.sidebar.multiselect(
    'Semestres:',
    options=sorted(df['semestre'].unique()),
    default=sorted(df['semestre'].unique())
)

df_filtrado = df[(df['grupo'].isin(grupos)) & (df['semestre'].isin(semestres))]

# Gráficos con Matplotlib/Seaborn
st.subheader("📊 Rendimiento por Materia")
materias = ['calificaciones_matematicas', 'calificaciones_ciencias', 
            'calificaciones_historia', 'calificaciones_espanol', 
            'calificaciones_ingles']

fig, ax = plt.subplots(figsize=(10, 5))
df_filtrado[materias].mean().plot(kind='bar', ax=ax, color='skyblue')
ax.set_ylabel('Promedio')
ax.set_title('Promedio por Materia')
st.pyplot(fig)

st.subheader("📈 Relación Asistencia vs Rendimiento")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.scatterplot(
    data=df_filtrado,
    x='porcentaje_asistencias',
    y='promedio_final',
    hue='grupo',
    ax=ax2
)
ax2.set_title('Asistencia vs Promedio Final')
st.pyplot(fig2)
