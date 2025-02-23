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
st.set_page_config(page_title="Tablero Indicadores CB", layout="wide")

# Agregar CSS personalizado con la fuente
st.markdown(
    f"""
    <style>
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
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Tablero de Indicadores - Corresponsales Bancarios")

# Reemplazar la sección de subida de archivo con lectura directa
archivo_path = os.path.join('Resultado', 'indicadores.xlsx')  # Ajusta el nombre del archivo según corresponda

try:
    # Cargar datos directamente desde el archivo local
    df = pd.read_excel(archivo_path)
    
    # 📌 Renombrar columnas para evitar problemas de espacios
    df.columns = ["Indicador", "REVAL", "VALE+", "Total"]

    # 📌 Crear filtro interactivo
    opcion_seleccionada = st.radio("Selecciona el tipo de dato:", ["VALE+", "REVAL", "Total"], horizontal=True)

    # 📌 Extraer valores específicos
    cantidad_total = df[df["Indicador"] == "Cantidad de puntos"]["Total"].values[0]
    cantidad_vale = df[df["Indicador"] == "Cantidad de puntos"]["VALE+"].values[0]
    cantidad_reval = df[df["Indicador"] == "Cantidad de puntos"]["REVAL"].values[0]

    # 📌 Calcular el porcentaje de participación
    porcentaje_vale = (cantidad_vale / cantidad_total) * 100
    porcentaje_reval = (cantidad_reval / cantidad_total) * 100

    # 📌 Crear columnas para distribuir contenido
    col1, col2, col3 = st.columns([1, 1, 1])

    # ✅ Mostrar el Total de la Red en una métrica grande
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

    # ✅ Mostrar el gráfico de barras con las opciones seleccionadas
    with col2:
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

except Exception as e:
    st.error(f"⚠️ Error al leer el archivo: {e}")
