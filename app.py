import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os
import plotly.graph_objects as go

# Función para convertir la fuente a base64
def get_font_base64(font_path):
    with open(font_path, 'rb') as font_file:
        return base64.b64encode(font_file.read()).decode()

# Ruta al archivo de la fuente
font_path = os.path.join('assets', 'CIBFONTSANS-REGULAR.OTF')
font_base64 = get_font_base64(font_path)

# Configuración de la página
st.set_page_config(
    page_title="Tablero Indicadores CB",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None
    }
)

# Agregar CSS personalizado con la fuente y tema oscuro
st.markdown(
    f"""
    <style>
        /* Tema oscuro forzado */
        .stApp {{
            background-color: #0E1117;
            color: white;
        }}
        
        /* Fuente personalizada */
        @font-face {{
            font-family: 'CIBFont';
            src: url(data:font/otf;base64,{font_base64}) format('opentype');
        }}
        
        * {{
            font-family: 'CIBFont', sans-serif !important;
        }}
        
        .stTitle {{
            font-family: 'CIBFont', sans-serif !important;
        }}
        
        div[data-testid="stMetricValue"] {{
            font-family: 'CIBFont', sans-serif !important;
        }}
        
        .plotly-graph-div {{
            font-family: 'CIBFont', sans-serif !important;
        }}

        /* Estilo para widgets */
        .stSelectbox label,
        .stRadio label {{
            color: white !important;
        }}

        .stMarkdown {{
            color: white;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.image("assets/Logotipo_Wompi_WH.png", width=200)

st.title(" 📈Tablero de Indicadores - Corresponsales Bancarios")

# Definir la ruta del archivo primero
archivo_path = os.path.join("Resultado", "informe_diario_20250222.xlsx")

# Obtener la fecha de última modificación del archivo
ultima_actualizacion = os.path.getmtime(archivo_path)
fecha_actualizacion = pd.to_datetime(ultima_actualizacion, unit='s').strftime("%d/%m/%Y %H:%M:%S")

# Mostrar la última actualización con estilo
st.markdown(
    f"""
    <div style="
        padding: 5px 15px;
        border-radius: 5px;
        background-color: rgba(255, 255, 255, 0.1);
        display: inline-block;
        margin-bottom: 20px;">
        <p style="margin: 0; color: #B0B0B0; font-size: 0.9em;">
            🕒 Última actualización: {fecha_actualizacion}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

try:
    # Cargar datos directamente desde el archivo local
    df = pd.read_excel(archivo_path)
    
    # 📌 Renombrar columnas para evitar problemas de espacios
    df.columns = ["Indicador", "REVAL", "VALE+", "Total"]

    # 📌 Crear filtro interactivo
    opcion_seleccionada = st.radio("Selecciona el tipo de dato:", ["VALE+", "REVAL", "Total"], horizontal=True)

    # 📌 Extraer valores específicos
    # Tamaño de red
    cantidad_total = df[df["Indicador"] == "Cantidad de puntos"]["Total"].values[0]
    cantidad_vale = df[df["Indicador"] == "Cantidad de puntos"]["VALE+"].values[0]
    cantidad_reval = df[df["Indicador"] == "Cantidad de puntos"]["REVAL"].values[0]

    # 📌Puntos bloqueados por no compensacion
    # puntos activos 
    seccion_bloqueo_activos_total = df[df["Indicador"] == "Puntos bloqueados - Activos"]["Total"].values[0]
    seccion_bloqueo_activos_vale = df[df["Indicador"] == "Puntos bloqueados - Activos"]["VALE+"].values[0]
    seccion_bloqueo_activos_reval = df[df["Indicador"] == "Puntos bloqueados - Activos"]["REVAL"].values[0]

    # puntos bloqueados
    seccion_bloqueo_bloqueados_total = df[df["Indicador"] == "Puntos bloqueados - Inactivos"]["Total"].values[0]
    seccion_bloqueo_bloqueados_vale = df[df["Indicador"] == "Puntos bloqueados - Inactivos"]["VALE+"].values[0]
    seccion_bloqueo_bloqueados_reval = df[df["Indicador"] == "Puntos bloqueados - Inactivos"]["REVAL"].values[0]

    # 📌 Puntos mala practica
    mala_practica_total = df[df["Indicador"] == "Puntos con malas prácticas (%)"]["Total"].values[0]
    mala_practica_vale = df[df["Indicador"] == "Puntos con malas prácticas (%)"]["VALE+"].values[0]
    mala_practica_reval = df[df["Indicador"] == "Puntos con malas prácticas (%)"]["REVAL"].values[0]



    # 📌 Calcular el porcentaje de participación
    porcentaje_vale = (cantidad_vale / cantidad_total) * 100
    porcentaje_reval = (cantidad_reval / cantidad_total) * 100

    # 📌 Crear columnas para distribuir contenido (primera fila)
    col1, col2, col3 = st.columns([1, 1, 1])

    # Primera fila de contenido
    with col1:
        valor_mostrar = {
            "VALE+": cantidad_vale,
            "REVAL": cantidad_reval,
            "Total": cantidad_vale + cantidad_reval
        }[opcion_seleccionada]
        
        st.markdown(
            f"""
            <div style="text-align: center">
                <p style="font-size:25px; margin-bottom:0px; font-weight:bold;">Tamaño de Red {opcion_seleccionada}</p>
                <p style="font-size:100px; font-weight:bold; margin-top:0px;">{valor_mostrar:,}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        # ✅ Mostrar el gráfico de barras con las opciones seleccionadas
        if opcion_seleccionada == "Total":
            # 📊 Gráfico de Barras mostrando ambas categorías (VALE+ y REVAL)
            datos_barra = pd.DataFrame({
                "Alianza": ["VALE+", "REVAL"],
                "Cantidad de Puntos": [cantidad_vale, cantidad_reval],
                "Porcentaje": [porcentaje_vale, porcentaje_reval]
            })

            fig = px.bar(
                datos_barra,
                y="Alianza",
                x="Cantidad de Puntos",
                width=480,
                height=320,
                color="Alianza",
                orientation='h',
                color_discrete_map={
                    "VALE+": "#00825A",
                    "REVAL": "#B0F2AE"
                }
            )

            # Agregar texto con valor y porcentaje dentro de cada barra
            fig.update_traces(
                texttemplate='<span style="font-size: 16px">%{x:,.0f}<br>(%{customdata:.1f}%)</span>',
                textposition="inside",
                customdata=datos_barra["Porcentaje"],
                textfont=dict(size=16, color="black"),
                insidetextanchor="middle"
            )

            # Centrar el título y hacerlo grande
            fig.update_layout(
                title=dict(text="Cantidad de Puntos por Aliado", x=0.5, font=dict(size=25, family="Arial", color="white")),
                xaxis=dict(title="Cantidad de Puntos"),
                yaxis=dict(title=""),
                margin=dict(l=20, r=20, t=50, b=20)
            )

        else:
            # 📊 Gráfico de Barra con el porcentaje de participación de un solo aliado
            datos_barra = pd.DataFrame({
                "Alianza": [opcion_seleccionada],
                "Participación (%)": [porcentaje_vale if opcion_seleccionada == "VALE+" else porcentaje_reval]
            })

            fig = px.bar(
                datos_barra,
                y="Alianza",
                x="Participación (%)",
                text_auto=".2f",
                width=480,
                height=320,
                orientation='h',
                color="Alianza",
                color_discrete_map={
                    "VALE+": "#00825A",
                    "REVAL": "#B0F2AE"
                }
            )

            fig.update_layout(
                title=dict(
                    text=f"Participación de {opcion_seleccionada} en la Red",
                    x=0.5,
                    y=0.95,
                    xanchor='center',
                    yanchor='top',
                    font=dict(size=25, family="Arial", color="white")
                ),
                xaxis=dict(range=[0, 100], title="Porcentaje de Red"),
                yaxis=dict(title=""),
                margin=dict(l=20, r=20, t=50, b=20)
            )

            # Agregar el símbolo de "%" a los valores
            fig.update_traces(
                texttemplate="%{x:.2f}%",
                textposition="outside",
                marker=dict(color="blue")
            )

        # Mostrar el gráfico con ancho fijo
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = valor_mostrar,
            title = {'text': f"Tamaño de Red {opcion_seleccionada}"},
            gauge = {'axis': {'range': [0, cantidad_total]},
                    'bar': {'color': "#00825A"}}
        ))
        st.plotly_chart(fig)

    # 📌 Crear columnas para distribuir contenido (segunda fila)
    col4, col5, col6 = st.columns([1, 1, 1])

    st.markdown("---")

    # Segunda fila de contenido
    with col4:
        # Seleccionar el valor según la opción
        valor_activos = {
            "VALE+": seccion_bloqueo_activos_vale,
            "REVAL": seccion_bloqueo_activos_reval,
            "Total": seccion_bloqueo_activos_total
        }[opcion_seleccionada]

        fig = go.Figure(go.Indicator(
            mode = "number+gauge+delta",
            gauge = {'shape': "bullet"},
            value = valor_activos,
            delta = {'reference': 200},
            domain = {'x': [0.1, 1], 'y': [0.2, 0.9]},
            title = {'text': f"Tamaño de Red {opcion_seleccionada}"}
        ))
        # Asegurarse de que el plotly_chart esté dentro del bloque 'with'
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        # Seleccionar el valor de puntos activos según la opción
        valor_activos = {
            "VALE+": seccion_bloqueo_activos_vale,
            "REVAL": seccion_bloqueo_activos_reval,
            "Total": seccion_bloqueo_activos_total
        }[opcion_seleccionada]

        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = valor_activos,  # Usar el valor de puntos activos
            title = {'text': f"Puntos Activos {opcion_seleccionada}"},
            gauge = {
                'axis': {'range': [0, 300]},  # Cambiado a 500
                'bar': {'color': "#00825A"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 250], 'color': 'lightgray'},  # Mitad de 500
                    {'range': [250, 500], 'color': 'gray'}      # Hasta 500
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 200  # 80% de 500
                }
            }
        ))

        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)
        
    with col6:
        # Seleccionar el valor de mala práctica según la opción, eliminar el % y convertir a float
        valor_mala_practica = float({
            "VALE+": str(mala_practica_vale).replace('%', ''),
            "REVAL": str(mala_practica_reval).replace('%', ''),
            "Total": str(mala_practica_total).replace('%', '')
        }[opcion_seleccionada])
        
        st.markdown(
            f"""
            <div style="
                background-color: #00825A;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <h3 style="color: white;">Mala Práctica {opcion_seleccionada}</h3>
                <h1 style="font-size: 3.5em; margin: 10px 0;">{valor_mala_practica:,.2f}%</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Crear un separador visual
    st.markdown("---")
    st.subheader("📍 Distribución Geográfica de Corresponsales")

    # Función para limpiar dataframes
    def limpiar_dataframe(df):
        df['Latitud'] = df['Latitud'].replace('', pd.NA)
        df['Longitud'] = df['Longitud'].replace('', pd.NA)
        df = df.dropna(subset=['Latitud', 'Longitud'])
        df['Codigo_Punto'] = df['Codigo_Punto'].astype(str)
        df['Aliado'] = df['Aliado'].astype(str)
        df['Latitud'] = df['Latitud'].astype(float)
        df['Longitud'] = df['Longitud'].astype(float)
        return df

    # Crear dos columnas para organizar los controles
    col_selector, col_stats = st.columns([3, 1])

    with col_selector:
        # Crear selector en Streamlit
        opcion_mapa = st.selectbox(
            'Seleccione el tipo de visualización:',
            ['Corresponsales uno a uno', 'Aperturas', 'Cierres']
        )

    # Leer los archivos usando rutas relativas
    df_base_completa = pd.read_csv('Resultado/df_base_completa.csv')
    
    df_base_cierres = pd.read_csv('Resultado/aperturas_20250223.csv')
    
    df_base_aperturas = pd.read_csv('Resultado/aperturas_20250223.csv')

    # Limpiar todos los dataframes
    df_base_completa = limpiar_dataframe(df_base_completa)
    df_base_cierres = limpiar_dataframe(df_base_cierres)
    df_base_aperturas = limpiar_dataframe(df_base_aperturas)

    # Función para crear mapa
    def crear_mapa(df, titulo):
        fig = px.scatter_map(
            df,
            lat='Latitud',
            lon='Longitud',
            hover_data=['Codigo_Punto', 'Aliado'],
            zoom=5,
            height=600,  # Reducido para mejor integración
            color='Aliado',
            title=titulo,
            color_discrete_map={
                "VALE+": "#00825A",
                "REVAL": "#B0F2AE"
            }
        )
        
        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox=dict(
                center=dict(lat=4.5709, lon=-74.2973),
            )
        )
        return fig

    # Mostrar mapa según selección
    if opcion_mapa == 'Corresponsales uno a uno':
        mapa = crear_mapa(df_base_completa, 'Distribución Total de Corresponsales')
        st.plotly_chart(mapa, use_container_width=True)
        
    elif opcion_mapa == 'Aperturas':
        mapa = crear_mapa(df_base_aperturas, 'Distribución de Aperturas')
        st.plotly_chart(mapa, use_container_width=True)
        
    else:  # Cierres
        mapa = crear_mapa(df_base_cierres, 'Distribución de Cierres')
        st.plotly_chart(mapa, use_container_width=True)

    with col_stats:
        # Mostrar estadísticas básicas
        st.markdown("### 📊 Estadísticas")
        if opcion_mapa == 'Corresponsales uno a uno':
            st.metric("Total de corresponsales", f"{len(df_base_completa):,}")
        elif opcion_mapa == 'Aperturas':
            st.metric("Total de aperturas", f"{len(df_base_aperturas):,}")
        else:
            st.metric("Total de cierres", f"{len(df_base_cierres):,}")

except Exception as e:
    st.error(f"⚠️ Error al leer el archivo: {e}")
