import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os
import plotly.graph_objects as go
from datetime import datetime

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
        /* Tema oscuro forzado - COMENTADO
        .stApp {{
            background-color: #0E1117;
            color: white;
        }}
        */
        
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
            color: inherit !important;
        }}

        .stMarkdown {{
            color: inherit;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Detectar el tema automáticamente usando CSS
st.markdown("""
    <style>
        /* Por defecto, mostrar el logo claro */
        #logo-claro { display: block; }
        #logo-oscuro { display: none; }
        
        /* En modo oscuro, invertir la visibilidad */
        @media (prefers-color-scheme: dark) {
            #logo-claro { display: none; }
            #logo-oscuro { display: block; }
        }
    </style>
""", unsafe_allow_html=True)

# Mostrar ambos logos con IDs para control de visibilidad
st.markdown(f"""
    <div id="logo-claro">
        <img src="data:image/png;base64,{base64.b64encode(open('assets/Logotipo_Wompi_VS2.png', 'rb').read()).decode()}" width="300">
    </div>
    <div id="logo-oscuro">
        <img src="data:image/png;base64,{base64.b64encode(open('assets/Logotipo_Wompi_WH.png', 'rb').read()).decode()}" width="300">
    </div>
""", unsafe_allow_html=True)

st.title(" 📈Tablero de Indicadores - Corresponsales Bancarios")

# Función para encontrar el archivo más reciente con un prefijo específico
def encontrar_archivo_reciente(directorio, prefijo):
    archivos = [f for f in os.listdir(directorio) if f.startswith(prefijo) and (f.endswith('.csv') or f.endswith('.xlsx'))]
    if not archivos:
        raise FileNotFoundError(f"No se encontraron archivos con prefijo {prefijo}")
    return os.path.join(directorio, max(archivos))  # max() devolverá el último archivo alfabéticamente (por fecha)

try:
    # Encontrar el archivo más reciente
    archivo_path = encontrar_archivo_reciente("Resultado", "informe_diario_")
    ultima_actualizacion = os.path.getmtime(archivo_path)
    fecha_actualizacion = datetime.fromtimestamp(ultima_actualizacion).strftime('%Y-%m-%d %H:%M:%S')
    
    # Leer el archivo Excel
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

    # 📌 Calcular el porcentaje de participación
    porcentaje_vale = (cantidad_vale / cantidad_total) * 100
    porcentaje_reval = (cantidad_reval / cantidad_total) * 100


    #NPS
    nps_total = float(str(df[df["Indicador"] == "NPS"]["Total"].values[0]).replace('%', ''))

    #ICX
    icx_total = df[df["Indicador"] == "ICX"]["Total"].values[0]


    # 📌Puntos bloqueados por no compensacion
    # puntos activos 
    Cantidad_de_puntos_total = df[df["Indicador"] == "Cantidad de puntos"]["Total"].values[0]
    Cantidad_de_puntos_vale = df[df["Indicador"] == "Cantidad de puntos"]["VALE+"].values[0]
    Cantidad_de_puntos_reval = df[df["Indicador"] == "Cantidad de puntos"]["REVAL"].values[0]

    # puntos bloqueados
    seccion_bloqueo_bloqueados_total = df[df["Indicador"] == "Puntos bloqueados - Inactivos"]["Total"].values[0]
    seccion_bloqueo_bloqueados_vale = df[df["Indicador"] == "Puntos bloqueados - Inactivos"]["VALE+"].values[0]
    seccion_bloqueo_bloqueados_reval = df[df["Indicador"] == "Puntos bloqueados - Inactivos"]["REVAL"].values[0]

    # Productividad
    productividad_total = df[df["Indicador"] == "Productividad - Cumple meta (%)"]["Total"].values[0]
    productividad_vale = df[df["Indicador"] == "Productividad - Cumple meta (%)"]["VALE+"].values[0]
    productividad_reval = df[df["Indicador"] == "Productividad - Cumple meta (%)"]["REVAL"].values[0]

    # SEGUROS
    seguros_total = df[df["Indicador"] == "Seguros mes actual"]["Total"].values[0]
    seguros_vale = df[df["Indicador"] == "Seguros mes actual"]["VALE+"].values[0]
    seguros_reval = df[df["Indicador"] == "Seguros mes actual"]["REVAL"].values[0]


    # 📌 Puntos mala practica
    mala_practica_total = df[df["Indicador"] == "Puntos con malas prácticas (%)"]["Total"].values[0]
    mala_practica_vale = df[df["Indicador"] == "Puntos con malas prácticas (%)"]["VALE+"].values[0]
    mala_practica_reval = df[df["Indicador"] == "Puntos con malas prácticas (%)"]["REVAL"].values[0]

    # 📌 Indicador tasa de activacion
    tasa_activacion_total = df[df["Indicador"] == "Puntos bloqueados - Activos (%)"]["Total"].values[0]
    tasa_activacion_vale = df[df["Indicador"] == "Puntos bloqueados - Activos (%)"]["VALE+"].values[0]
    tasa_activacion_reval = df[df["Indicador"] == "Puntos bloqueados - Activos (%)"]["REVAL"].values[0]

    # Aperturas 
    aperturas_total = df[df["Indicador"] == "Aperturas del mes"]["Total"].values[0]
    aperturas_vale = df[df["Indicador"] == "Aperturas del mes"]["VALE+"].values[0]
    aperturas_reval = df[df["Indicador"] == "Aperturas del mes"]["REVAL"].values[0]

    # Cierres
    cierres_total = df[df["Indicador"] == "Cierres del mes"]["Total"].values[0]
    cierres_vale = df[df["Indicador"] == "Cierres del mes"]["VALE+"].values[0]
    cierres_reval = df[df["Indicador"] == "Cierres del mes"]["REVAL"].values[0]


    # 📌 Crear columnas para distribuir contenido (primera fila)
    st.markdown("---")

    # Primera fila - Valor único centrado
    valor_mostrar = {
    "VALE+": Cantidad_de_puntos_vale,
    "REVAL": Cantidad_de_puntos_reval,
    "Total": Cantidad_de_puntos_total
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

    st.markdown("---")

    # Segunda fila - 3 columnas
    col2, col3, col4 = st.columns([1, 1, 1])

    with col2:
        # Gauge para NPS
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = nps_total,
            title = {
                'text': "NPS",
                'font': {
                    'size': 24,
                    'weight': 'bold'
                }
            },
            number = {'suffix': '%', 'font': {'size': 50}},  # Aumentando tamaño del número
            gauge = {
                'axis': {'range': [-100, 100]},
                'bar': {'color': "#99D1FC", 'thickness': 0.90},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [-100, 0], 'color': "#FF4B4B"},
                    {'range': [0, 50], 'color': "#FAFAFA"},
                    {'range': [50, 100], 'color': "#B0F2AE"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        fig.update_layout(
        height=300,  # Aumentando un poco la altura
        margin=dict(t=50, b=30, l=20, r=20)  # Aumentando el margen superior
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        # Gauge para ICX
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = float(icx_total),
            title = {
                'text': "ICX",
                'font': {
                    'size': 24,
                    'weight': 'bold'
                }
            },
            number = {'font': {'size': 50}},  # Aumentando tamaño del número
            gauge = {
                'axis': {'range': [0, 5]},
                'bar': {'color': "#99D1FC", 'thickness': 0.90},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 2.5], 'color': "#FF4B4B"},
                    {'range': [2.5, 4], 'color': "#FAFAFA"},
                    {'range': [4, 5], 'color': "#B0F2AE"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 4
                }
            }
        ))
        fig.update_layout(
            height=300,  # Aumentando un poco la altura
            margin=dict(t=50, b=30, l=20, r=20)  # Aumentando el margen superior
        )
        st.plotly_chart(fig, use_container_width=True)


    with col4:
        # Tercer gauge
        valor_mala_practica = float({
            "VALE+": str(mala_practica_vale).replace('%', ''),
            "REVAL": str(mala_practica_reval).replace('%', ''),
            "Total": str(mala_practica_total).replace('%', '')
        }[opcion_seleccionada])

        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = valor_mala_practica,
            title = {
                'text': f"Mala Práctica {opcion_seleccionada}",
                'font': {
                    'size': 24,
                    'weight': 'bold'
                }
            },
            number = {'suffix': '%', 'font': {'size': 50}},  # Aumentando tamaño del número
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#99D1FC", 'thickness': 0.90},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': "#FAFAFA"},
                    {'range': [50, 100], 'color': "#B0F2AE"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        fig.update_layout(
            height=300,  # Aumentando un poco la altura
            margin=dict(t=50, b=30, l=20, r=20)  # Aumentando el margen superior
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Tercera fila - 3 columnas
    col5, col6, col7 = st.columns([1, 1, 1])

    with col5:
        # Gauge para Productividad
        productividad_df = df[df["Indicador"] == "Productividad - Cumple meta (%)"]["Total"].values[0]
        productividad_total = float(str(productividad_df).replace('%', ''))

        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = productividad_total,
            title = {
                'text': "Productividad",
                'font': {
                    'size': 24,
                    'weight': 'bold'
                }
            },
            number = {'suffix': '%', 'font': {'size': 50}},  # Tamaño número aumentado
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#99D1FC", 'thickness': 0.90},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 40], 'color': "#FF4B4B"},
                    {'range': [40, 70], 'color': "#FAFAFA"},
                    {'range': [70, 100], 'color': "#B0F2AE"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig.update_layout(
            height=300,  # Altura aumentada
            margin=dict(t=50, b=30, l=20, r=20)  # Margen superior aumentado
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col6: # SEGUROS
        # Seleccionar el valor de puntos activos según la opción
        valor_activos = {
            "VALE+": seguros_vale,
            "REVAL": seguros_reval,
            "Total": seguros_total
        }[opcion_seleccionada]
        
        st.markdown(
            f"""
            <div style="text-align: center">
                <p style="font-size:25px; margin-bottom:20px; font-weight:bold;">Seguros {opcion_seleccionada}</p>
                <p style="font-size:100px; font-weight:bold; margin-top:20px;">{valor_activos:,}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col7: # PUNTOS BLOQUEADOS
        # Gauge para Puntos Bloqueados
        puntos_bloqueados_total = df[df["Indicador"] == "Puntos con malas prácticas (%)"]["Total"].values[0]
        puntos_bloqueados_valor_total = float(str(puntos_bloqueados_total).replace('%', ''))
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = puntos_bloqueados_valor_total,
            title = {
                'text': "Puntos Bloqueados",
                'font': {
                    'size': 24,
                    'weight': 'bold'
                }
            },
            number = {'suffix': '%', 'font': {'size': 50}},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#99D1FC", 'thickness': 0.90},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 40], 'color': "#B0F2AE"},
                    {'range': [40, 70], 'color': "#FAFAFA"},
                    {'range': [70, 100], 'color': "#FF4B4B"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig.update_layout(
            height=300,
            margin=dict(t=50, b=30, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Cuarta fila - 3 columnas
    col8, col9, col10 = st.columns([1, 1, 1])

    with col8:
        # Gauge para Puntos bloqueados - Activos
        puntos_bloqueados_df = df[df["Indicador"] == "Puntos bloqueados - Activos (%)"]["Total"].values[0]
        puntos_bloqueados_valor = float(str(puntos_bloqueados_df).replace('%', ''))
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = puntos_bloqueados_valor,
            title = {
                'text': "Índice de Activación",
                'font': {
                    'size': 24,
                    'weight': 'bold'
                }
            },
            number = {'suffix': '%', 'font': {'size': 50}},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#99D1FC", 'thickness': 0.90},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 40], 'color': "#FF4B4B"},
                    {'range': [40, 70], 'color': "#FAFAFA"},
                    {'range': [70, 100], 'color': "#B0F2AE"} # rojo claro
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig.update_layout(
            height=300,
            margin=dict(t=50, b=30, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col9: # APERTURAS
        datos_pie = pd.DataFrame({
            'Alianza': ['VALE+', 'REVAL'],
            'Aperturas': [aperturas_vale, aperturas_reval]
        })
        
        fig = px.pie(
            datos_pie,
            values='Aperturas',
            names='Alianza',
            title='Aperturas',
            color='Alianza',
            color_discrete_map={
                "VALE+": "#00825A",
                "REVAL": "#B0F2AE"
            },
            height=300
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='value+percent',
            textfont_size=14,
            hole=0.4,
        )
        
        fig.update_layout(
            title={
                'text': 'Aperturas',
                'x': 0.5,
                'y': 0.95,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {
                    'size': 24,
                    'weight': 'bold'
                }
            },
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            margin=dict(t=50, b=50, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col10:
        datos_pie = pd.DataFrame({
            'Alianza': ['VALE+', 'REVAL'],
            'Cierres': [cierres_vale, cierres_reval]
        })
        
        fig = px.pie(
            datos_pie,
            values='Cierres',
            names='Alianza',
            title='Cierres',
            color='Alianza',
            color_discrete_map={
                "VALE+": "#00825A",
                "REVAL": "#B0F2AE"
            },
            height=300
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='value+percent',
            textfont_size=14,
            hole=0.4,
        )
        
        fig.update_layout(
            title={
                'text': 'Cierres',
                'x': 0.5,
                'y': 0.95,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {
                    'size': 24,
                    'weight': 'bold'
                }
            },
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            margin=dict(t=50, b=50, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader(" 📍Distribución Geográfica de Corresponsales")

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

    # Crear columnas para organizar los controles
    col_selector, col_filter, col_map_type, col_stats = st.columns([2, 1, 1, 1])

    with col_selector:
        # Actualizar selector para incluir "Todos"
        opcion_mapa = st.selectbox(
            'Seleccione el tipo de visualización:',
            ['Todos', 'Aperturas', 'Cierres']
        )
    
    with col_filter:
        # Agregar filtro para REVAL/VALE+
        opcion_aliado = st.selectbox(
            'Seleccione el aliado:',
            ['Todos', 'VALE+', 'REVAL']
        )

    with col_map_type:
        # Agregar selector de tipo de mapa
        tipo_mapa = st.selectbox(
            'Tipo de Mapa:',
            ['Puntos', 'Densidad']
        )

    try:
        # Encontrar los archivos más recientes
        ruta_aperturas = encontrar_archivo_reciente("Resultado", "aperturas_")
        ruta_cierres = encontrar_archivo_reciente("Resultado", "cierres_")

        # Leer los archivos usando las rutas encontradas
        df_base_cierres = pd.read_csv(ruta_cierres)
        df_base_aperturas = pd.read_csv(ruta_aperturas)
        df_base_cierres.rename(columns={'Fuerza_Comercial': 'Aliado'}, inplace=True)
        df_base_aperturas.rename(columns={'Fuerza_Comercial': 'Aliado'}, inplace=True)

        # Mostrar la fecha de última actualización basada en el archivo de aperturas
        ultima_actualizacion = os.path.getmtime(ruta_aperturas)
        fecha_actualizacion = pd.to_datetime(ultima_actualizacion, unit='s').strftime("%d/%m/%Y %H:%M:%S")

        # Limpiar los dataframes
        df_base_cierres = limpiar_dataframe(df_base_cierres)
        df_base_aperturas = limpiar_dataframe(df_base_aperturas)

        # Función para crear mapa de puntos
        def crear_mapa_puntos(df, titulo):
            # Filtrar por aliado si se seleccionó uno específico
            if opcion_aliado != 'Todos':
                df = df[df['Aliado'] == opcion_aliado]

            if opcion_mapa == 'Todos':
                # Para vista 'Todos', colorear por tipo
                fig = px.scatter_mapbox(
                    df,
                    lat='Latitud',
                    lon='Longitud',
                    hover_data={
                        'Codigo_Punto': True,
                        'Aliado': True,
                        'Tipo': True,
                        'Latitud': False,
                        'Longitud': False
                    },
                    color='Tipo',
                    color_discrete_map={
                        'Apertura': '#00825A',  # Verde para aperturas
                        'Cierre': '#7d1b18'     # Rojo para cierres
                    },
                    zoom=5,
                    height=600,
                    title=titulo
                )
            else:
                # Para vistas individuales, colorear por aliado
                fig = px.scatter_mapbox(
                    df,
                    lat='Latitud',
                    lon='Longitud',
                    hover_data={
                        'Codigo_Punto': True,
                        'Aliado': True,
                        'Tipo': True,
                        'Latitud': False,
                        'Longitud': False
                    },
                    color='Aliado',
                    color_discrete_map={
                        "VALE+": "#00825A" if opcion_mapa == 'Aperturas' else "#7d1b18",
                        "REVAL": "#B0F2AE" if opcion_mapa == 'Aperturas' else "#d4150f"
                    },
                    zoom=5,
                    height=600,
                    title=titulo
                )
            
            fig.update_layout(
                # mapbox_style="carto-positron",
                mapbox_style="open-street-map",
                mapbox=dict(
                    center=dict(lat=4.5709, lon=-74.2973),
                ),
                modebar_remove=["zoomIn", "zoomOut"],  # Mantener solo los controles necesarios
                dragmode='pan'  # Permitir arrastrar el mapa
            )
            
            fig.update_traces(
                marker=dict(
                    size=10,
                    opacity=0.7
                ),
                selector=dict(mode='markers'),
                hovertemplate="<b>Código Punto:</b> %{customdata[0]}<br><b>Aliado:</b> %{customdata[1]}<br><b>Tipo:</b> %{customdata[2]}<br><extra></extra>"
            )
            
            return fig

        # Función para crear mapa de densidad
        def crear_mapa_densidad(df, titulo):
            # Filtrar por aliado si se seleccionó uno específico
            if opcion_aliado != 'Todos':
                df = df[df['Aliado'] == opcion_aliado]

            # Redondear coordenadas para agrupar puntos cercanos (2 decimales para más agrupamiento)
            df['Latitud_round'] = df['Latitud'].round(2)
            df['Longitud_round'] = df['Longitud'].round(2)

            # Crear un DataFrame con el conteo de puntos por ubicación
            density_df = df.groupby(['Latitud_round', 'Longitud_round']).agg({
                'Tipo': 'count',
                'Latitud': 'first',
                'Longitud': 'first'
            }).reset_index()
            
            density_df.rename(columns={'Tipo': 'count'}, inplace=True)

            # Escala de colores fríos a cálidos
            color_scale = [
                [0, '#313695'],    # Azul oscuro
                [0.2, '#4575B4'],  # Azul medio
                [0.4, '#74ADD1'],  # Azul claro
                [0.6, '#FED976'],  # Amarillo
                [0.8, '#FD8D3C'],  # Naranja
                [1.0, '#BD0026']   # Rojo intenso
            ]

            # Radio unificado para todas las vistas
            radius_val = 50  # Aumentado para mejor visualización

            fig = px.density_mapbox(
                density_df,
                lat='Latitud',
                lon='Longitud',
                z='count',
                radius=radius_val,
                zoom=5,
                height=600,
                title=titulo,
                opacity=0.9,
                color_continuous_scale=color_scale
            )

            fig.update_layout(
                mapbox_style="carto-positron",
                mapbox=dict(
                    center=dict(lat=4.5709, lon=-74.2973),
                ),
                modebar_remove=["zoomIn", "zoomOut"],  # Mantener solo los controles necesarios
                dragmode='pan'  # Permitir arrastrar el mapa
            )

            # Ocultar la información del hover
            fig.update_traces(
                hoverinfo='none',
                hovertemplate=None
            )

            return fig
        
        # Modificar la lógica de visualización del mapa
        if opcion_mapa == 'Todos':
            # Combinar dataframes de aperturas y cierres
            df_base_aperturas['Tipo'] = 'Apertura'
            df_base_cierres['Tipo'] = 'Cierre'
            df_combinado = pd.concat([df_base_aperturas, df_base_cierres])
            
            if tipo_mapa == 'Puntos':
                mapa = crear_mapa_puntos(df_combinado, 'Distribución de Aperturas y Cierres')
            else:
                mapa = crear_mapa_densidad(df_combinado, 'Densidad de Aperturas y Cierres')
                
        elif opcion_mapa == 'Aperturas':
            df_base_aperturas['Tipo'] = 'Apertura'
            
            if tipo_mapa == 'Puntos':
                mapa = crear_mapa_puntos(df_base_aperturas, 'Distribución de Aperturas')
            else:
                mapa = crear_mapa_densidad(df_base_aperturas, 'Densidad de Aperturas')
                
        else:  # Cierres
            df_base_cierres['Tipo'] = 'Cierre'
            
            if tipo_mapa == 'Puntos':
                mapa = crear_mapa_puntos(df_base_cierres, 'Distribución de Cierres')
            else:
                mapa = crear_mapa_densidad(df_base_cierres, 'Densidad de Cierres')

        st.plotly_chart(mapa, use_container_width=True, config={'scrollZoom': True})

        with col_stats:
            # Actualizar estadísticas para incluir vista combinada
            st.markdown("### 📊 Estadísticas")
            if opcion_mapa == 'Todos':
                df_filtered = df_combinado if opcion_aliado == 'Todos' else df_combinado[df_combinado['Aliado'] == opcion_aliado]
                st.metric("Total de puntos", f"{len(df_filtered):,}")
            elif opcion_mapa == 'Aperturas':
                df_filtered = df_base_aperturas if opcion_aliado == 'Todos' else df_base_aperturas[df_base_aperturas['Aliado'] == opcion_aliado]
                st.metric("Total de aperturas", f"{len(df_filtered):,}")
            else:
                df_filtered = df_base_cierres if opcion_aliado == 'Todos' else df_base_cierres[df_base_cierres['Aliado'] == opcion_aliado]
                st.metric("Total de cierres", f"{len(df_filtered):,}")

    except FileNotFoundError:
        st.error("No se encontró el archivo de informe diario en la carpeta Resultado")
        st.stop()
    except Exception as e:
        st.error(f"Error al leer el archivo: {str(e)}")
        st.stop()

except Exception as e:
    st.error(f"⚠️ Error al leer el archivo: {e}")

except FileNotFoundError:
    st.error("No se encontró el archivo de informe diario en la carpeta Resultado")
    st.stop()
except Exception as e:
    st.error(f"Error al leer el archivo: {str(e)}")
    st.stop()
