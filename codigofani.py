import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(page_title="Analizador Académico", layout="wide", page_icon="📚")
st.title("📚 Analizador Académico Avanzado")

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv('unidos.csv')

df = cargar_datos()

# Limpieza de datos
df['porcentaje_asistencias'] = df['porcentaje_asistencias'].round(1)
df['promedio_final'] = df['promedio_final'].round(1)

# Sidebar con filtros
st.sidebar.header('🔍 Filtros Avanzados')

# Filtros múltiples
grupos_seleccionados = st.sidebar.multiselect(
    'Grupos:',
    options=sorted(df['grupo'].unique()),
    default=sorted(df['grupo'].unique())
)

semestres_seleccionados = st.sidebar.multiselect(
    'Semestres:',
    options=sorted(df['semestre'].unique()),
    default=sorted(df['semestre'].unique())
)

# Filtro de rendimiento mínimo
umbral_aprobacion = st.sidebar.slider(
    'Umbral de aprobación:',
    min_value=0,
    max_value=100,
    value=70
)

# Función para calcular estudiantes destacados
def obtener_destacados(dataframe, umbral):
    return dataframe[dataframe['promedio_final'] >= umbral]

# Función para análisis por materia
def analisis_materias(dataframe):
    materias = ['calificaciones_matematicas', 'calificaciones_ciencias', 
                'calificaciones_historia', 'calificaciones_espanol', 
                'calificaciones_ingles']
    return dataframe[materias].mean().reset_index().rename(columns={'index':'Materia', 0:'Promedio'})

# Aplicar filtros
df_filtrado = df[
    (df['grupo'].isin(grupos_seleccionados)) & 
    (df['semestre'].isin(semestres_seleccionados))
]

# Mostrar métricas clave
st.subheader('📊 Resumen General')
col1, col2, col3 = st.columns(3)
col1.metric("Total Estudiantes", len(df_filtrado))
col2.metric("Promedio General", f"{df_filtrado['promedio_final'].mean():.1f}")
col3.metric("Asistencia Promedio", f"{df_filtrado['porcentaje_asistencias'].mean():.1f}%")

# Pestañas para organizar el contenido
tab1, tab2, tab3 = st.tabs(["📈 Rendimiento", "📊 Comparativas", "👥 Estudiantes"])

with tab1:
    # Gráfico de rendimiento por materia
    st.subheader("📚 Rendimiento por Materia")
    
    df_materias = analisis_materias(df_filtrado)
    fig1 = px.bar(
        df_materias,
        x='Materia',
        y='Promedio',
        color='Promedio',
        color_continuous_scale='Viridis',
        title='Promedio por Materia'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico de correlación
    st.subheader("🔗 Correlación entre Materias")
    materias = ['calificaciones_matematicas', 'calificaciones_ciencias', 
                'calificaciones_historia', 'calificaciones_espanol', 
                'calificaciones_ingles']
    fig2 = px.imshow(
        df_filtrado[materias].corr(),
        text_auto=True,
        color_continuous_scale='Blues',
        title='Correlación entre Materias'
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    # Comparativa entre grupos
    st.subheader("🆚 Comparativa entre Grupos")
    
    fig3 = px.box(
        df_filtrado,
        x='grupo',
        y='promedio_final',
        color='grupo',
        points='all',
        title='Distribución de Promedios por Grupo'
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # Evolución por semestre
    st.subheader("🔄 Evolución por Semestre")
    evolucion = df_filtrado.groupby('semestre').agg({
        'promedio_final': 'mean',
        'porcentaje_asistencias': 'mean'
    }).reset_index()
    
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig4.add_trace(
        go.Scatter(
            x=evolucion['semestre'],
            y=evolucion['promedio_final'],
            name='Promedio Académico',
            mode='lines+markers',
            line=dict(color='#636EFA')
        ),
        secondary_y=False
    )
    
    fig4.add_trace(
        go.Scatter(
            x=evolucion['semestre'],
            y=evolucion['porcentaje_asistencias'],
            name='Asistencia (%)',
            mode='lines+markers',
            line=dict(color='#FF7F0E')
        ),
        secondary_y=True
    )
    
    fig4.update_layout(
        title_text='Evolución del Rendimiento',
        xaxis_title='Semestre',
        hovermode='x unified'
    )
    
    fig4.update_yaxes(title_text="Promedio Académico", secondary_y=False)
    fig4.update_yaxes(title_text="Asistencia (%)", secondary_y=True)
    
    st.plotly_chart(fig4, use_container_width=True)

with tab3:
    # Estudiantes destacados
    st.subheader("🏆 Estudiantes Destacados")
    destacados = obtener_destacados(df_filtrado, umbral_aprobacion)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Estudiantes destacados", 
            f"{len(destacados)} ({len(destacados)/len(df_filtrado)*100:.1f}%)"
        )
    
    with col2:
        st.metric(
            "Promedio de destacados", 
            f"{destacados['promedio_final'].mean():.1f}"
        )
    
    # Tabla interactiva de estudiantes
    st.dataframe(
        destacados.sort_values('promedio_final', ascending=False),
        column_config={
            "nombre": "Estudiante",
            "promedio_final": st.column_config.NumberColumn("Promedio", format="%.1f"),
            "porcentaje_asistencias": st.column_config.NumberColumn("Asistencia", format="%.1f%%")
        },
        hide_index=True,
        use_container_width=True
    )

# Pie de página
st.markdown("---")
st.caption("Herramienta de análisis académico desarrollada con Streamlit | © 2023")