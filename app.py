import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os
import plotly.graph_objects as go
from datetime import datetime
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader



# 📌 Configuración de la página - DEBE SER EL PRIMER COMANDO DE STREAMLIT
st.set_page_config(
    page_title="Tablero Indicadores CB",
    layout="wide",
    initial_sidebar_state="expanded"
)

# # Ocultar barra superior de Streamlit (incluye "Manage app")
# st.markdown(
#     """
#     <style>
#     header {visibility: hidden;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )


# 📌 Función para obtener la configuración
def get_config():
    # try:
    # Intentar usar secrets de Streamlit (para la nube)
    config = {
        "credentials": {
            "usernames": {
                # Usuario 1
                st.secrets["auth"]["users"]["slenis"]["username"]: {
                    "email": st.secrets["auth"]["users"]["slenis"]["email"],
                    "name": st.secrets["auth"]["users"]["slenis"]["name"],
                    "password": st.secrets["auth"]["users"]["slenis"]["password"],
                    "role": st.secrets["auth"]["users"]["slenis"]["role"]
                },
                # Usuario 2
                st.secrets["auth"]["users"]["wileon"]["username"]: {
                    "email": st.secrets["auth"]["users"]["wileon"]["email"],
                    "name": st.secrets["auth"]["users"]["wileon"]["name"],
                    "password": st.secrets["auth"]["users"]["wileon"]["password"],
                    "role": st.secrets["auth"]["users"]["wileon"]["role"]
                },
                # Usuario 3
                st.secrets["auth"]["users"]["yalibele"]["username"]: {
                    "email": st.secrets["auth"]["users"]["yalibele"]["email"],
                    "name": st.secrets["auth"]["users"]["yalibele"]["name"],
                    "password": st.secrets["auth"]["users"]["yalibele"]["password"],
                    "role": st.secrets["auth"]["users"]["yalibele"]["role"]
                },           
                # Usuario 4
                st.secrets["auth"]["users"]["dorgutie"]["username"]: {
                    "email": st.secrets["auth"]["users"]["dorgutie"]["email"],
                    "name": st.secrets["auth"]["users"]["dorgutie"]["name"],
                    "password": st.secrets["auth"]["users"]["dorgutie"]["password"],
                    "role": st.secrets["auth"]["users"]["dorgutie"]["role"]
                },
                # Usuario 5
                st.secrets["auth"]["users"]["magvalen"]["username"]: {
                    "email": st.secrets["auth"]["users"]["magvalen"]["email"],
                    "name": st.secrets["auth"]["users"]["magvalen"]["name"],
                    "password": st.secrets["auth"]["users"]["magvalen"]["password"],
                    "role": st.secrets["auth"]["users"]["magvalen"]["role"]
                },
                # Usuario 6
                st.secrets["auth"]["users"]["clrestre"]["username"]: {
                    "email": st.secrets["auth"]["users"]["clrestre"]["email"],
                    "name": st.secrets["auth"]["users"]["clrestre"]["name"],
                    "password": st.secrets["auth"]["users"]["clrestre"]["password"],
                    "role": st.secrets["auth"]["users"]["clrestre"]["role"]
                }
            }
        },
        "cookie": {
            "expiry_days": st.secrets["cookie"]["expiry_days"],
            "key": st.secrets["cookie"]["key"],
            "name": st.secrets["cookie"]["name"]
        }
    }
    # except:
    #     # Si falla, usar config.yaml local
    #     with open('config.yaml') as file:
    #         config = yaml.load(file, Loader=SafeLoader)
    
    return config

# 📌 Obtener configuración
config = get_config()

# 📌 Crear el autenticador
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# with open('config.yaml', 'w') as file:
#     yaml.dump(config, file, default_flow_style=False, allow_unicode=True)





try:
    authenticator.login(fields={'Form name':'Login', 'Username':'Usuario', 'Password':'Contraseña', 'Login':'Ingresar'})
except Exception as e:
    st.error(e)


if st.session_state.get('authentication_status'):
    #authenticator.logout()
    st.write(f'Bienvenido *{st.session_state.get("name")}*')

    if st.button("🚪 Cerrar sesión"):
        authenticator.logout()
        st.session_state["authentication_status"] = None  # 🔹 Restablecer el estado de sesión
        st.session_state["username"] = None
        st.rerun()  




    # Obtener el rol del usuario actual
    username = st.session_state.get("username")
    user_role = config["credentials"]["usernames"][username]["role"]
       
    # Contenido basado en roles
    if user_role == "admin":
        st.title("Panel de Administración")
        # ... resto del código para admin ...
        
    if user_role in ["admin", "editor"]:
        st.header("Edición de Datos")

    else:
        st.title("Modo Visualización")

    if user_role == "admin":
        st.success("🔐 Modo Administrador Activo")  # Mensaje en verde
    elif user_role == "editor":
        st.info("✏️ Modo Editor Activo")  # Mensaje en azul
    else:  # viewer
        st.warning("👀 Modo Visualización Activo")  # Mensaje en amarillo

    # Función para convertir la fuente a base64
    def get_font_base64(font_path):
        with open(font_path, 'rb') as font_file:
            return base64.b64encode(font_file.read()).decode()

    # Ruta al archivo de la fuente
    font_path = os.path.join('assets', 'CIBFONTSANS-REGULAR.OTF')
    font_base64 = get_font_base64(font_path)

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

    st.markdown(
        "<h2 style='text-align: center;'>📈 Tablero de Indicadores - Corresponsales Bancarios</h2>",
        unsafe_allow_html=True
)

    # Definir la ruta base usando secrets
    BASE_PATH = st.secrets.get("BASE_PATH", os.getcwd())
    RESULTADO_DIR = os.path.join(BASE_PATH, "Resultado")

    def encontrar_archivo_reciente(directorio, prefijo):
        """
        Encuentra el archivo más reciente con manejo de rutas absolutas
        """
        try:
            # Usar ruta absoluta
            ruta_absoluta = os.path.join(BASE_PATH, directorio)
            
            # Debug para verificar rutas
            st.write(f"Buscando en: {ruta_absoluta}")
            st.write(f"Buscando archivos con prefijo: {prefijo}")
            
            if not os.path.exists(ruta_absoluta):
                st.error(f"Directorio no encontrado: {ruta_absoluta}")
                return None

            archivos = [f for f in os.listdir(ruta_absoluta) 
                       if f.startswith(prefijo) and (f.endswith('.csv') or f.endswith('.xlsx'))]
            
            if not archivos:
                st.warning(f"No se encontraron archivos con prefijo {prefijo}")
                return None

            archivo_reciente = max(archivos)
            return os.path.join(ruta_absoluta, archivo_reciente)

        except Exception as e:
            st.error(f"Error al buscar archivo: {str(e)}")
            return None

    # 📌 Crear filtro interactivo
    col_filter_month, col_filter_type = st.columns([1, 1])

    with col_filter_type:
        opcion_seleccionada = st.selectbox(
            "Selecciona el tipo de dato:",
            ["VALE+", "REVAL", "Total"]
        )

    with col_filter_month:
        # Obtener el mes actual
        mes_actual = datetime.now().month
        año_actual = datetime.now().year
        last_year = año_actual - 1  # Para siempre mostrar el año siguiente
        
        # Crear lista de meses disponibles hasta el mes actual
        meses = {
            1: 'Enero',
            2: 'Febrero',
            3: 'Marzo',
            4: 'Abril',
            5: 'Mayo',
            6: 'Junio',
            7: 'Julio',
            8: 'Agosto',
            9: 'Septiembre',
            10: 'Octubre',
            11: 'Noviembre',
            12: 'Diciembre'
        }
        
        meses_disponibles = {k: v for k, v in meses.items() if k <= mes_actual}
        
        mes_seleccionado = st.selectbox(
            "Selecciona el mes:",
            list(meses_disponibles.values()),
            index=len(meses_disponibles) - 1  # Seleccionar el mes actual por defecto
        )
        
        # Convertir el mes seleccionado a número
        mes_numero = list(meses.keys())[list(meses.values()).index(mes_seleccionado)]

    def obtener_archivo_por_mes(mes_numero, mes_nombre):
        try:
            # Debug: mostrar qué estamos buscando
            st.write(f"Buscando archivo para mes: {mes_nombre} (número: {mes_numero})")
            
            año_actual = datetime.now().year
            mes_lower = mes_nombre.lower()
            
            # Construir patrones de búsqueda más flexibles
            patrones = [
                f"informe_mensual_{mes_lower}_{año_actual}",      # informe_mensual_enero_2025
                f"informe_mensual_{mes_lower}_{año_actual-1}",    # informe_mensual_enero_2024
                f"informe_diario_{año_actual}{mes_numero:02d}",   # informe_diario_202501
                f"informe_mensual_{mes_lower}",                   # informe_mensual_enero
                f"informe_{mes_lower}_{año_actual}",              # informe_enero_2025
                f"informe_{mes_lower}"                            # informe_enero
            ]
            
            # Buscar en la carpeta Resultado
            for archivo in os.listdir("Resultado"):
                # Debug: mostrar cada archivo encontrado
                st.write(f"Revisando archivo: {archivo}")
                
                # Verificar si alguno de los patrones coincide
                for patron in patrones:
                    if archivo.lower().startswith(patron.lower()) and (archivo.endswith('.xlsx') or archivo.endswith('.xls')):
                        ruta_completa = os.path.join("Resultado", archivo)
                        st.write(f"¡Archivo encontrado!: {ruta_completa}")
                        return ruta_completa
            
            # Si no se encontró ningún archivo
            st.warning(f"No se encontró ningún archivo para {mes_nombre}")
            return None
            
        except Exception as e:
            st.error(f"Error buscando archivo: {str(e)}")
            st.write("Detalles del error:", str(e))
            return None

    # Función auxiliar para listar todos los archivos en el directorio
    def mostrar_archivos_disponibles():
        st.write("Archivos disponibles en el directorio Resultado:")
        try:
            archivos = os.listdir("Resultado")
            for archivo in archivos:
                st.write(f"- {archivo}")
        except Exception as e:
            st.error(f"Error al listar archivos: {str(e)}")

    # Llamar a la función auxiliar antes de buscar el archivo
    mostrar_archivos_disponibles()

    def obtener_datos_mes_anterior(mes_numero, año_actual):
        """
        Obtiene los datos del mes anterior, manejando el cambio de año
        """
        try:
            # Calcular mes anterior y año
            if mes_numero == 1:
                mes_anterior = 12
                año_anterior = año_actual - 1
            else:
                mes_anterior = mes_numero - 1
                año_anterior = año_actual
                
            mes_anterior_nombre = meses[mes_anterior].lower()
            
            # Debug
            st.write(f"Buscando datos del mes anterior: {mes_anterior_nombre} {año_anterior}")
            
            # Intentar obtener archivo del mes anterior
            archivo_anterior = obtener_archivo_por_mes(mes_anterior, meses[mes_anterior])
            
            if archivo_anterior:
                df_anterior = pd.read_excel(archivo_anterior)
                df_anterior.columns = ["Indicador", "REVAL", "VALE+", "Total"]
                return df_anterior
            
            return None
            
        except Exception as e:
            st.write(f"Error obteniendo datos del mes anterior: {str(e)}")
            return None

    try:
        # Obtener la ruta del archivo según el mes seleccionado
        archivo_path = obtener_archivo_por_mes(mes_numero, mes_seleccionado)
        
        if archivo_path is None:
            # Mostrar mensaje de error amigable y deshabilitar la selección
            st.error(f"⚠️ Los datos para {mes_seleccionado} aún no están disponibles.")
            st.info("👉 Por favor seleccione otro mes disponible.")
            st.stop()  # Detener la ejecución aquí
        
        # Si llegamos aquí, el archivo existe
        df = pd.read_excel(archivo_path)
        
        # Opcional: mostrar qué archivo se está usando
        st.caption(f"📊 Mostrando datos de: {os.path.basename(archivo_path)}")
        
        # Si el nombre del archivo no incluye el mes, puedes filtrar los datos después de leerlos
        if 'Fecha' in df.columns:  # Si tienes una columna de fecha
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            df = df[df['Fecha'].dt.month == mes_numero]
        
        # 📌 Renombrar columnas para evitar problemas de espacios
        df.columns = ["Indicador", "REVAL", "VALE+", "Total"]

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


        # # 📌Puntos bloqueados por no compensacion
        # # puntos activos 
        # Cantidad_de_puntos_total = df[df["Indicador"] == "Cantidad de puntos"]["Total"].values[0]
        # Cantidad_de_puntos_vale = df[df["Indicador"] == "Cantidad de puntos"]["VALE+"].values[0]
        # Cantidad_de_puntos_reval = df[df["Indicador"] == "Cantidad de puntos"]["REVAL"].values[0]

        # centidad de transacciones
        n_trx_total = df[df["Indicador"] == "Número de transacciones"]["Total"].values[0]
        n_trx_vale = df[df["Indicador"] == "Número de transacciones"]["VALE+"].values[0]
        n_trx_reval = df[df["Indicador"] == "Número de transacciones"]["REVAL"].values[0]

        # valor de transacciones
        monto_total = df[df["Indicador"] == "Valor transacciones"]["Total"].values[0]
        monto_vale = df[df["Indicador"] == "Valor transacciones"]["VALE+"].values[0]
        monto_reval = df[df["Indicador"] == "Valor transacciones"]["REVAL"].values[0]

        # # puntos bloqueados
        # seccion_bloqueo_bloqueados_total = df[df["Indicador"] == "Puntos bloqueados - Inactivos"]["Total"].values[0]
        # seccion_bloqueo_bloqueados_vale = df[df["Indicador"] == "Puntos bloqueados - Inactivos"]["VALE+"].values[0]
        # seccion_bloqueo_bloqueados_reval = df[df["Indicador"] == "Puntos bloqueados - Inactivos"]["REVAL"].values[0]

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

        bloqueos_total = df[df["Indicador"] == "Bloqueos"]["Total"].values[0]
        bloqueos_vale = df[df["Indicador"] == "Bloqueos"]["VALE+"].values[0]
        bloqueos_reval = df[df["Indicador"] == "Bloqueos"]["REVAL"].values[0]

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

        #metas
        meta_nps = 79.32
        meta_icx = 4.77
        meta_bloqueos_no_compensacion = 2.0
        meta_mala_practica = 2.95
        meta_productividad = 53
        meta_tamaño_red = 17081
        meta_seguros = 2300 
        meta_tasa_activacion = 70

        trx_2024 = {
            1: {"mes": "Enero",
                "n_trx": 37451738,
                "n_trx_vale": 20362784,
                "n_trx_reval": 17088954,
                "monto_total": 12531612050035.30,
                "monto_vale": 6670867004567.79,
                "monto_reval": 5860745045467.51,
                "tamano_red": 17615,
                "tamano_vale": 8930,
                "tamano_reval": 8685

            },
            2: {"mes": "Febrero",
                "n_trx": 39334971,
                "n_trx_vale": 21419611,
                "n_trx_reval": 17915360,
                "monto_total": 12796654863197.60,
                "monto_vale": 6847684973185.17,
                "monto_reval": 5948969890012.46,
                "tamano_red": 17400,
                "tamano_vale": 8830,
                "tamano_reval": 8570
            },
            3: {"mes": "Marzo",
                "n_trx": 41024457,
                "n_trx_vale": 22341051,
                "n_trx_reval": 18703406,
                "monto_total": 13198739185854.20,
                "monto_vale": 7083410119567.39,
                "monto_reval": 6115329066286.84,
                "tamano_red": 17273,
                "tamano_vale": 8831,
                "tamano_reval": 8442
            },
            4: {"mes": "Abril",
                "n_trx": 43062654,
                "n_trx_vale": 23164659,
                "n_trx_reval": 19897995,
                "monto_total": 13908932924068.70,
                "monto_vale": 7380116781315.09,
                "monto_reval": 6528816142753.63,
                "tamano_red": 17124,
                "tamano_vale": 8817,
                "tamano_reval": 8307
            },
            5: {"mes": "Mayo",
                "n_trx": 44206422,
                "n_trx_vale": 23953864,
                "n_trx_reval": 20252558,
                "monto_total": 14243805538789.80,
                "monto_vale": 7595871431090.04,
                "monto_reval": 6647934107699.84,
                "tamano_red": 17020,
                "tamano_vale": 8746,
                "tamano_reval": 8274
            },
            6: {"mes": "Junio",
                "n_trx": 40699748,
                "n_trx_vale": 22137382,
                "n_trx_reval": 18562366,
                "monto_total": 13586307429958.00,
                "monto_vale": 7285525516986.00,
                "monto_reval": 6300781912972.00,
                "tamano_red": 17081,
                "tamano_vale": 8761,
                "tamano_reval": 8320
            },
            7: {"mes": "Julio",
                "n_trx": 43727597,
                "n_trx_vale": 23591316,
                "n_trx_reval": 20134281,
                "monto_total": 14629032017464.30,
                "monto_vale": 7785002382081.35,
                "monto_reval": 6844029635383.00,
                "tamano_red": 17024,
                "tamano_vale": 8758,
                "tamano_reval": 8266
            },
            8: {"mes": "Agosto",
                "n_trx": 44087671,
                "n_trx_vale": 23790532,
                "n_trx_reval": 20392139,
                "monto_total": 14503442933175.50,
                "monto_vale": 7715309415515.50,
                "monto_reval": 6788133517660.00,
                "tamano_red": 17111,
                "tamano_vale": 8806,
                "tamano_reval": 8305
            },
            9: {"mes": "Septiembre",
                "n_trx": 43453537,
                "n_trx_vale": 23488235,
                "n_trx_reval": 19965302,
                "monto_total": 13996580009696.00,
                "monto_vale": 7478005410242.00,
                "monto_reval": 6518574599454.00,
                "tamano_red": 16969,
                "tamano_vale": 8736,
                "tamano_reval": 8233
            },
            10: {"mes": "Octubre",
                "n_trx": 45406935,
                "n_trx_vale": 24466908,
                "n_trx_reval": 20940027,
                "monto_total": 15029944063064.00,
                "monto_vale": 7945033888498.00,
                "monto_reval": 7084910174566.00,
                "tamano_red": 16876,
                "tamano_vale": 8734,
                "tamano_reval": 8142
            },
            11: {"mes": "Noviembre",
                "n_trx": 43950267,
                "n_trx_vale": 23667858,
                "n_trx_reval": 20282409,
                "monto_total": 14946992943494.00,
                "monto_vale": 7944534214050.00,
                "monto_reval": 7002458729444.00,
                "tamano_red": 16882,
                "tamano_vale": 8762,
                "tamano_reval": 8140
            },
            12: {"mes": "Diciembre",
                "n_trx": 44699007,
                "n_trx_vale": 24052185,
                "n_trx_reval": 20646822,
                "monto_total": 16954503228177.00,
                "monto_vale": 8976899635297.00,
                "monto_reval": 7977603592880.00,
                "tamano_red": 17081,
                "tamano_vale": 8797,
                "tamano_reval": 8184
            }
        }


        def calcular_variacion_porcentual(valor_actual, valor_anterior):
            """Calcula la variación porcentual entre dos valores"""
            if valor_anterior == 0:
                return 0
            return ((valor_actual - valor_anterior) / valor_anterior) * 100

        def crear_indicador_numerico(valor_mostrar, meta, titulo, mostrar_delta=True):
            """
            Crea un indicador numérico con Plotly
            
            Args:
                valor_mostrar: Valor actual a mostrar
                meta: Valor objetivo o meta
                titulo: Título del indicador
                mostrar_delta: Si se debe mostrar la variación porcentual (True/False)
            """
            if mostrar_delta:
                delta_config = {
                    "reference": meta,
                    # "relative": True,
                    "valueformat": ".1f%%",
                    "increasing": {"color": "green"},
                    "decreasing": {"color": "red"}
                }
                mode = "number+delta"
            else:
                delta_config = None
                mode = "number"

            fig = go.Figure(go.Indicator(
                mode=mode,
                value=valor_mostrar,
                number={"valueformat": ",", "font": {"size": 80}},
                delta=delta_config,
                title={
                    "text": titulo,
                    "font": {
                        "size": 24
                    }
                },
                domain={"x": [0, 1], "y": [0, 1]}
            ))

            fig.add_annotation(
                text=f"Meta: {meta:,}",
                x=0.5, y=0.1,
                showarrow=False,
                font=dict(size=22, color="gray")
            )
            
            return fig

        def crear_gauge(valor, titulo, meta, rango_max, mostrar_porcentaje=True):
            """
            Crea un gráfico tipo gauge con Plotly
            
            Args:
                valor: Valor actual a mostrar
                titulo: Título del gauge
                meta: Valor objetivo o meta
                rango_max: Valor máximo del rango
                mostrar_porcentaje: Si se debe mostrar el símbolo de porcentaje
            """
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=valor,
                title={
                    'text': titulo,
                    'font': {
                        'size': 24
                    }
                },
                number={'suffix': '%' if mostrar_porcentaje else '', 'font': {'size': 50}},
                gauge={
                    'axis': {'range': [0, rango_max]},
                    'bar': {'color': "#99D1FC", 'thickness': 0.90},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, meta], 'color': "#FF4B4B"},
                        {'range': [meta, rango_max], 'color': "#B0F2AE"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': meta
                    }
                }
            ))
            
            fig.update_layout(
                height=300,
                margin=dict(t=50, b=30, l=20, r=20)
            )
            
            return fig

        def crear_grafico_pie(valores_vale, valores_reval, titulo, nombre_valor):
            """
            Crea un gráfico de tipo pie con Plotly Express
            
            Args:
                valores_vale: Valor para VALE+
                valores_reval: Valor para REVAL
                titulo: Título del gráfico
                nombre_valor: Nombre de la columna de valores (ej: 'Aperturas', 'Cierres')
            """
            datos_pie = pd.DataFrame({
                'Alianza': ['VALE+', 'REVAL'],
                nombre_valor: [valores_vale, valores_reval]
            })
            
            fig = px.pie(
                datos_pie,
                values=nombre_valor,
                names='Alianza',
                title=titulo,
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
                    'text': titulo,
                    'x': 0.5,
                    'y': 0.95,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {
                        'size': 24,
                        'weight': 'normal'
                    }
                },
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                margin=dict(t=50, b=50, l=20, r=20)
            )
            
            return fig

        def crear_bullet_chart(valor_mostrar, meta, titulo, nombre_indicador):
            """
            Crea un gráfico de tipo bullet chart con Plotly
            
            Args:
                valor_mostrar: Valor actual a mostrar
                meta: Valor objetivo o meta
                titulo: Título del gráfico
                nombre_indicador: Nombre del indicador para mostrar en el eje Y
            """
            fig = go.Figure()
            
            # Agregar la barra principal
            fig.add_trace(go.Bar(
                x=[valor_mostrar],
                y=[nombre_indicador],
                orientation='h',
                marker=dict(
                    color='#FF4B4B' if valor_mostrar > meta else '#B0F2AE',
                    line=dict(color='black', width=2)
                ),
                text=f'{valor_mostrar:.1f}%',
                textposition='outside',
                textfont=dict(
                    size=24
                ),
                width=0.4,
                name=f'Valor Actual: {valor_mostrar:.1f}%'
            ))
            
            # Agregar línea vertical de limite
            fig.add_shape(
                type='line',
                x0=meta, x1=meta,
                y0=-0.5, y1=0.5,
                line=dict(color='red', width=4, dash='dash')
            )

            # Añadir anotación para el valor del limite
            fig.add_annotation(
                x=max(valor_mostrar, meta) * 1.1,
                y=0,
                text=f'Limite: {meta}%',
                showarrow=False,
                font=dict(
                    size=16,
                    color='red'
                ),
                xanchor='left',
                yanchor='middle'
            )

            # Actualizar el layout
            fig.update_layout(
                title={
                    'text': titulo,
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {
                        'size': 20,  # Reducido de 28 a 20
                        'weight': 'normal'
                    }
                },
                dragmode=False,  # 🔹 Evita zoom en el Bullet Chart
                height=300,
                margin=dict(t=50, b=30, l=20, r=150),
                xaxis=dict(
                    title=dict(
                        text='Porcentaje (%)',
                        font=dict(size=16)
                    ),
                    range=[0, max(valor_mostrar, meta) * 1.1],
                    showgrid=True,
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    tickfont=dict(size=14),
                    showticklabels=True
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    range=[-0.5, 0.5]
                ),
                showlegend=False,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02
                ),
                plot_bgcolor=None,
                paper_bgcolor=None
            )
            
            return fig
        
        def abreviar_numero(valor):
            """
            Convierte números grandes en formato abreviado con sufijos en español.
            Siempre devuelve un número y un sufijo.
            """
            try:
                valor = float(valor)  # Asegurar que sea numérico
                if valor >= 1e12:
                    return round(valor / 1e12, 2), " B"  # Billones
                elif valor >= 1e9:
                    return round(valor / 1e9, 2), " MM"  # Mil millones
                elif valor >= 1e6:
                    return round(valor / 1e6, 2), " M"  # Millones
                elif valor >= 1e3:
                    return round(valor / 1e3, 2), " K"  # Miles
                else:
                    return round(valor, 2), ""  # Número sin abreviar
            except Exception as e:
                return valor, ""  # En caso de error, devuelve el número original sin sufijo


        def indicador_con_variacion(valor_actual, var_mes_anterior, var_anio_anterior, titulo):
            """
            Crea un indicador que muestra el valor actual y sus variaciones
            
            Args:
                valor_actual: Valor numérico a mostrar
                var_mes_anterior: Variación porcentual respecto al mes anterior
                var_anio_anterior: Variación porcentual respecto al año anterior
                titulo: Título del indicador
            """
            # Determinar colores según las variaciones
            color_mes_anterior = "green" if var_mes_anterior >= 0 else "red"
            color_anio_anterior = "green" if var_anio_anterior >= 0 else "red"
            
            fig = go.Figure()

            # Valor Principal
            fig.add_trace(go.Indicator(
                mode="number",
                value=valor_actual,
                number={
                    "valueformat": ",",
                    "font": {"size": 60}
                },
                title={
                    "text": titulo,
                    "font": {"size": 24}
                },
                domain={"x": [0, 1], "y": [0.6, 1]}
            ))

            # Variación vs Mes anterior
            fig.add_annotation(
                text=f"{'▲' if var_mes_anterior >= 0 else '▼'} {abs(var_mes_anterior):.1f}% vs Mes anterior",
                x=0.5,
                y=0.45,
                showarrow=False,
                font={
                    "size": 20,
                    "color": color_mes_anterior
                },
                xref='paper',
                yref='paper'
            )

            # Variación vs Año anterior
            fig.add_annotation(
                text=f"{'▲' if var_anio_anterior >= 0 else '▼'} {abs(var_anio_anterior):.1f}% vs Año anterior",
                x=0.5,
                y=0.3,
                showarrow=False,
                font={
                    "size": 20,
                    "color": color_anio_anterior
                },
                xref='paper',
                yref='paper'
            )

            # Actualizar el layout
            fig.update_layout(
                height=350,
                margin=dict(t=40, b=40, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            return fig



        def abreviar_numero(valor):
            """
            Convierte números grandes en formato abreviado con sufijos en español.
            Siempre devuelve un número y un sufijo.
            """
            try:
                valor = float(valor)  # Asegurar que sea numérico
                if valor >= 1e12:
                    return round(valor / 1e12, 2), " B"  # Billones
                elif valor >= 1e9:
                    return round(valor / 1e9, 2), " MM"  # Mil millones
                elif valor >= 1e6:
                    return round(valor / 1e6, 2), " M"  # Millones
                elif valor >= 1e3:
                    return round(valor / 1e3, 2), " K"  # Miles
                else:
                    return round(valor, 2), ""  # Número sin abreviar
            except Exception as e:
                return valor, ""  # En caso de error, devuelve el número original sin sufijo



        def es_mes_historico(mes_num, mes_act):
            """
            Determina si el mes seleccionado es histórico
            """
            try:
                mes_num = int(mes_num)
                mes_act = int(mes_act)
                return mes_num < mes_act
            except (ValueError, TypeError):
                return False

        # 📌 Crear columnas para distribuir contenido (primera fila)
        st.markdown("---")

        # Primera fila - Tres columnas
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            mes_actual_num = int(datetime.now().month)
            es_historico = es_mes_historico(mes_numero, mes_actual_num)
            
            if es_mes_historico(mes_numero, mes_actual_num):
                # Seleccionar el valor según la opción elegida
                if opcion_seleccionada == "VALE+":
                    valor_actual = cantidad_vale
                    valor_2024 = trx_2024[mes_numero]["tamano_vale"]
                    titulo = "Tamaño de Red VALE+"
                    # Debug prints
                    st.write(f"Valor actual VALE+ (mes seleccionado): {valor_actual:,d}")
                    st.write(f"Valor mismo mes año anterior VALE+: {valor_2024:,d}")
                elif opcion_seleccionada == "REVAL":
                    valor_actual = cantidad_reval
                    valor_2024 = trx_2024[mes_numero]["tamano_reval"]
                    titulo = "Tamaño de Red REVAL"
                    # Debug prints
                    st.write(f"Valor actual REVAL (mes seleccionado): {valor_actual:,d}")
                    st.write(f"Valor mismo mes año anterior REVAL: {valor_2024:,d}")
                else:  # Total
                    valor_actual = cantidad_total
                    valor_2024 = trx_2024[mes_numero]["tamano_red"]
                    titulo = "Tamaño de Red"
                    # Debug prints
                    st.write(f"Valor actual Total (mes seleccionado): {cantidad_total:,d}")
                    st.write(f"Valor mismo mes año anterior Total: {trx_2024[mes_numero]['tamano_red']:,d}")

                try:
                    # Comparar con el mismo mes del año siguiente
                    var_anio_anterior = calcular_variacion_porcentual(valor_actual, valor_2024)
                    
                    # Comparar con el mes anterior
                    mes_anterior = mes_numero - 1 if mes_numero > 1 else 12
                    archivo_mes_anterior = obtener_archivo_por_mes(mes_anterior, meses[mes_anterior])
                    if archivo_mes_anterior:
                        df_anterior = pd.read_excel(archivo_mes_anterior)
                        if opcion_seleccionada == "VALE+":
                            valor_mes_anterior = df_anterior[df_anterior["Indicador"] == "Cantidad de puntos"]["VALE+"].values[0]
                        elif opcion_seleccionada == "REVAL":
                            valor_mes_anterior = df_anterior[df_anterior["Indicador"] == "Cantidad de puntos"]["REVAL"].values[0]
                        else:
                            valor_mes_anterior = df_anterior[df_anterior["Indicador"] == "Cantidad de puntos"]["Total"].values[0]
                        
                        st.write(f"Valor mes anterior {opcion_seleccionada}: {valor_mes_anterior:,d}")
                        var_mes_anterior = calcular_variacion_porcentual(valor_actual, valor_mes_anterior)
                    else:
                        var_mes_anterior = 0
                        st.warning(f"No se encontró información para el mes anterior")
                    
                    fig1 = indicador_con_variacion(
                        valor_actual=valor_actual,
                        var_mes_anterior=var_mes_anterior,
                        var_anio_anterior=var_anio_anterior,
                        titulo=titulo
                    )
                    st.plotly_chart(fig1, use_container_width=True, key=f"tamaño_red_{opcion_seleccionada}")
                except Exception as e:
                    st.error(f"Error al procesar tamaño de red histórico: {str(e)}")
            else:
                # Para mes actual (marzo)
                if opcion_seleccionada == "VALE+":
                    valor_actual = trx_2024[3]["tamano_vale"]
                    titulo = "Tamaño de Red VALE+"
                    st.write(f"Valor actual VALE+ (marzo): {valor_actual:,d}")
                elif opcion_seleccionada == "REVAL":
                    valor_actual = trx_2024[3]["tamano_reval"]
                    titulo = "Tamaño de Red REVAL"
                    st.write(f"Valor actual REVAL (marzo): {valor_actual:,d}")
                else:
                    valor_actual = trx_2024[3]["tamano_red"]
                    titulo = "Tamaño de Red"
                    st.write(f"Valor actual Total (marzo): {valor_actual:,d}")

                try:
                    fig1 = go.Figure(go.Indicator(
                        mode="number",
                        value=valor_actual,
                        number={'valueformat': ",", 'font': {'size': 50}},
                        title={'text': titulo, 'font': {'size': 20}},
                    ))
                    fig1.update_layout(height=350)
                    st.plotly_chart(fig1, use_container_width=True, key=f"tamaño_red_actual_{opcion_seleccionada}")
                except Exception as e:
                    st.error(f"Error al procesar tamaño de red actual: {str(e)}")

        with col2:
            if es_mes_historico(mes_numero, mes_actual_num):
                # Seleccionar el valor según la opción elegida
                if opcion_seleccionada == "VALE+":
                    valor_actual = n_trx_vale
                    valor_2024 = trx_2024[mes_numero]["n_trx_vale"]
                    titulo = "Transacciones VALE+"
                    # Debug prints
                    st.write(f"Valor actual VALE+ (mes seleccionado): {valor_actual:,d}")
                    st.write(f"Valor mismo mes año anterior VALE+: {valor_2024:,d}")
                elif opcion_seleccionada == "REVAL":
                    valor_actual = n_trx_reval
                    valor_2024 = trx_2024[mes_numero]["n_trx_reval"]
                    titulo = "Transacciones REVAL"
                    # Debug prints
                    st.write(f"Valor actual REVAL (mes seleccionado): {valor_actual:,d}")
                    st.write(f"Valor mismo mes año anterior REVAL: {valor_2024:,d}")
                else:  # Total
                    valor_actual = n_trx_total
                    valor_2024 = trx_2024[mes_numero]["n_trx"]
                    titulo = "Transacciones"
                    # Debug prints
                    st.write(f"Valor actual Total (mes seleccionado): {valor_actual:,d}")
                    st.write(f"Valor mismo mes año anterior Total: {valor_2024:,d}")

                try:
                    var_anio_anterior = calcular_variacion_porcentual(valor_actual, valor_2024)
                    
                    mes_anterior = mes_numero - 1 if mes_numero > 1 else 12
                    archivo_mes_anterior = obtener_archivo_por_mes(mes_anterior, meses[mes_anterior])
                    if archivo_mes_anterior:
                        df_anterior = pd.read_excel(archivo_mes_anterior)
                        if opcion_seleccionada == "VALE+":
                            valor_mes_anterior = df_anterior[df_anterior["Indicador"] == "Número de transacciones"]["VALE+"].values[0]
                        elif opcion_seleccionada == "REVAL":
                            valor_mes_anterior = df_anterior[df_anterior["Indicador"] == "Número de transacciones"]["REVAL"].values[0]
                        else:
                            valor_mes_anterior = df_anterior[df_anterior["Indicador"] == "Número de transacciones"]["Total"].values[0]
                        
                        st.write(f"Valor mes anterior {opcion_seleccionada}: {valor_mes_anterior:,d}")
                        var_mes_anterior = calcular_variacion_porcentual(valor_actual, valor_mes_anterior)
                    else:
                        var_mes_anterior = 0
                        st.warning(f"No se encontró información para el mes anterior")
                    
                    fig2 = indicador_con_variacion(
                        valor_actual=valor_actual,
                        var_mes_anterior=var_mes_anterior,
                        var_anio_anterior=var_anio_anterior,
                        titulo=titulo
                    )
                    st.plotly_chart(fig2, use_container_width=True, key=f"transacciones_{opcion_seleccionada}")
                except Exception as e:
                    st.error(f"Error al procesar transacciones histórico: {str(e)}")
            else:
                # Para mes actual (marzo)
                if opcion_seleccionada == "VALE+":
                    valor_actual = trx_2024[3]["n_trx_vale"]
                    titulo = "Transacciones VALE+"
                    st.write(f"Valor actual VALE+ (marzo): {trx_2024[3]['n_trx_vale']:,d}")
                elif opcion_seleccionada == "REVAL":
                    valor_actual = trx_2024[3]["n_trx_reval"]
                    titulo = "Transacciones REVAL"
                    st.write(f"Valor actual REVAL (marzo): {trx_2024[3]['n_trx_reval']:,d}")
                else:
                    valor_actual = trx_2024[3]["n_trx"]
                    titulo = "Transacciones"
                    st.write(f"Valor actual Total (marzo): {trx_2024[3]['n_trx']:,d}")

                try:
                    fig2 = go.Figure(go.Indicator(
                        mode="number",
                        value=valor_actual,
                        number={'valueformat': ",", 'font': {'size': 50}},
                        title={'text': titulo, 'font': {'size': 20}},
                    ))
                    fig2.update_layout(height=350)
                    st.plotly_chart(fig2, use_container_width=True, key=f"transacciones_actual_{opcion_seleccionada}")
                except Exception as e:
                    st.error("Error al procesar transacciones actual")

        with col3:
            try:
                if es_mes_historico(mes_numero, mes_actual_num):
                    # 📌 Obtener el valor actual según la opción seleccionada
                    if opcion_seleccionada == "VALE+":
                        valor_actual = float(str(monto_vale).replace(',', ''))
                        valor_2024 = float(str(trx_2024[mes_numero]["monto_vale"]).replace(',', ''))
                        titulo = "Montos VALE+"
                    elif opcion_seleccionada == "REVAL":
                        valor_actual = float(str(monto_reval).replace(',', ''))
                        valor_2024 = float(str(trx_2024[mes_numero]["monto_reval"]).replace(',', ''))
                        titulo = "Montos REVAL"
                    else:  # Total
                        valor_actual = float(str(monto_total).replace(',', ''))
                        valor_2024 = float(str(trx_2024[mes_numero]["monto_total"]).replace(',', ''))
                        titulo = "Montos"

                    # 📌 Debug con valores separados por miles
                    st.write(f"Valor actual {opcion_seleccionada} (mes seleccionado): {'{:,.0f}'.format(valor_actual)}")
                    st.write(f"Valor mismo mes año anterior {opcion_seleccionada}: {'{:,.0f}'.format(valor_2024)}")

                    # 📌 Abreviar valores correctamente
                    valor_actual_abrev, sufijo_actual = abreviar_numero(valor_actual)
                    valor_2024_abrev, sufijo_2024 = abreviar_numero(valor_2024)

                    # 📌 Variaciones
                    var_anio_anterior = calcular_variacion_porcentual(valor_actual, valor_2024)

                    # 📌 Obtener el valor del mes anterior si existe
                    mes_anterior = mes_numero - 1 if mes_numero > 1 else 12
                    archivo_mes_anterior = obtener_archivo_por_mes(mes_anterior, meses[mes_anterior])

                    if archivo_mes_anterior:
                        df_anterior = pd.read_excel(archivo_mes_anterior)
                        columna = opcion_seleccionada if opcion_seleccionada != "Total" else "Total"
                        valor_mes_anterior = float(str(df_anterior[df_anterior["Indicador"] == "Valor transacciones"][columna].values[0]).replace(',', ''))
                        valor_mes_anterior_abrev, sufijo_anterior = abreviar_numero(valor_mes_anterior)
                        var_mes_anterior = calcular_variacion_porcentual(valor_actual, valor_mes_anterior)

                        # 📌 Debug con separadores de miles
                        st.write(f"Valor mes anterior {opcion_seleccionada}: {'{:,.0f}'.format(valor_mes_anterior)}")

                    else:
                        var_mes_anterior = 0
                        st.warning(f"No se encontró información para el mes anterior")

                    # 📌 Gráfico con variaciones
                    fig3 = indicador_con_variacion(
                        valor_actual=valor_actual_abrev,  # ✅ Valor abreviado
                        var_mes_anterior=var_mes_anterior,
                        var_anio_anterior=var_anio_anterior,
                        titulo=titulo
                    )

                    fig3.update_traces(
                        number={
                            "prefix": "$",
                            "valueformat": ".2f",
                            "suffix": sufijo_actual,  # ✅ Usa el sufijo correcto
                            "font": {"size": 60}
                        }
                    )

                    st.plotly_chart(fig3, use_container_width=True, key=f"montos_{opcion_seleccionada}")

                else:
                    # 📌 Para mes actual (Marzo), mostrar solo el valor sin debug ni variaciones
                    if opcion_seleccionada == "VALE+":
                        valor_actual = float(str(trx_2024[3]["monto_vale"]).replace(',', ''))
                        titulo = "Montos VALE+"
                    elif opcion_seleccionada == "REVAL":
                        valor_actual = float(str(trx_2024[3]["monto_reval"]).replace(',', ''))
                        titulo = "Montos REVAL"
                    else:
                        valor_actual = float(str(trx_2024[3]["monto_total"]).replace(',', ''))
                        titulo = "Montos"

                    # 📌 Debug con separadores de miles
                    st.write(f"Valor actual {opcion_seleccionada} (marzo): {'{:,.0f}'.format(valor_actual)}")

                    # 📌 Aplicar la abreviación correctamente
                    valor_actual_abrev, sufijo_actual = abreviar_numero(valor_actual)

                    fig3 = go.Figure(go.Indicator(
                        mode="number",
                        value=valor_actual_abrev,  # ✅ Usa el valor abreviado
                        number={
                            'prefix': "$",
                            'valueformat': ".2f",
                            'suffix': sufijo_actual,  # ✅ Usa el sufijo correcto
                            'font': {'size': 50}
                        },
                        title={'text': titulo, 'font': {'size': 20}},
                    ))
                    fig3.update_layout(height=350)
                    st.plotly_chart(fig3, use_container_width=True, key=f"montos_actual_{opcion_seleccionada}")

            except Exception as e:
                st.error(f"❌ Error al procesar montos: {str(e)}")


        st.markdown("---")

        #Segunda fila - 3 columnas
        col4, col5, col6 = st.columns([1, 1, 1])

        with col4:
            # Gauge para NPS
            fig = crear_gauge(
                valor=nps_total,
                titulo="NPS",
                meta=meta_nps,
                rango_max=100
            )
            st.plotly_chart(fig, use_container_width=True)

        with col5:
            # Gauge para ICX
            fig = crear_gauge(
                valor=float(icx_total),
                titulo="ICX",
                meta=meta_icx,
                rango_max=5,
                mostrar_porcentaje=False
            )
            
            st.plotly_chart(fig, use_container_width=True)


        with col6:
            # Crear gráfico de bullet chart para bloqueos por no compensacion    
            valor_mostrar = {
                "VALE+": float(str(bloqueos_vale).replace('%', '')),
                "REVAL": float(str(bloqueos_reval).replace('%', '')),
                "Total": float(str(bloqueos_total).replace('%', ''))
            }[opcion_seleccionada]
            
            fig = crear_bullet_chart(
                valor_mostrar=valor_mostrar,
                meta=meta_bloqueos_no_compensacion,
                titulo='Bloqueos por no compensacion',
                nombre_indicador='Bloqueos por no compensacion'
            )
            
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': False,  # Oculta la barra de herramientas
                'scrollZoom': False,      # Deshabilita el zoom con scroll
                'doubleClick': False      # Deshabilita el zoom con doble click
            })

        st.markdown("---")

        # Tercera fila - 3 columnas
        col7, col8, col9 = st.columns([1, 1, 1])

        with col7:
            # Gauge para Productividad
            productividad_df = df[df["Indicador"] == "Productividad - Cumple meta (%)"]["Total"].values[0]
            productividad_total = float(str(productividad_df).replace('%', ''))

            fig = crear_gauge(
                valor=productividad_total,
                titulo="Productividad",
                meta=meta_productividad,
                rango_max=100
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col8: # SEGUROS
            # Seleccionar el valor de puntos activos según la opción
            valor_activos = {
                "VALE+": seguros_vale,
                "REVAL": seguros_reval,
                "Total": seguros_total
            }[opcion_seleccionada]

            # Crear y mostrar el indicador de seguros
            fig = crear_indicador_numerico(
                valor_mostrar=valor_activos,
                meta=meta_seguros,
                titulo=f"Seguros {opcion_seleccionada}",
                mostrar_delta=(opcion_seleccionada == "Total")
            )
            # 📌 Mostrar en Streamlit
            st.plotly_chart(fig, use_container_width=True)

        with col9: # MALA PRACTICA
            valor_mostrar = {
                "VALE+": float(str(mala_practica_vale).replace('%', '')),
                "REVAL": float(str(mala_practica_reval).replace('%', '')),
                "Total": float(str(mala_practica_total).replace('%', ''))
            }[opcion_seleccionada]
            
            fig = crear_bullet_chart(
                valor_mostrar=valor_mostrar,
                meta=meta_mala_practica,
                titulo=f'Mala Práctica - {opcion_seleccionada}',
                nombre_indicador='Mala Práctica'
            )
            
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': False,  # Oculta la barra de herramientas
                'scrollZoom': False,      # Deshabilita el zoom con scroll
                'doubleClick': False      # Deshabilita el zoom con doble click
            })


        st.markdown("---")

        # Cuarta fila - 3 columnas
        col10, col11, col12 = st.columns([1, 1, 1])

        with col10:
            # Gauge para Puntos bloqueados - Activos
            puntos_bloqueados_df = df[df["Indicador"] == "Puntos bloqueados - Activos (%)"]["Total"].values[0]
            
            fig = crear_gauge(
                valor=float(str(puntos_bloqueados_df).replace('%', '')),
                titulo="Puntos bloqueados - Activos",
                meta=meta_tasa_activacion,  #revisar tasa de activacion
                rango_max=100
            )
            st.plotly_chart(fig, use_container_width=True)

        with col11: # APERTURAS
            fig = crear_grafico_pie(
                valores_vale=aperturas_vale,
                valores_reval=aperturas_reval,
                titulo='Aperturas',
                nombre_valor='Aperturas'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col12: # CIERRES
            fig = crear_grafico_pie(
                valores_vale=cierres_vale,
                valores_reval=cierres_reval,
                titulo='Cierres',
                nombre_valor='Cierres'
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
            # Construir el nombre del archivo según el mes seleccionado
            mes_actual = datetime.now().month
            año_actual = datetime.now().year
            
            # Si es mes actual, buscar archivos con formato actual
            if mes_numero == mes_actual:
                ruta_aperturas = encontrar_archivo_reciente("Resultado", "aperturas_")
                ruta_cierres = encontrar_archivo_reciente("Resultado", "cierres_")
            else:
                # Para meses anteriores, buscar archivos con formato mes_[NombreMes]
                nombre_mes = meses[mes_numero].lower()
                ruta_aperturas = os.path.join("Resultado", f"aperturas_mes_{nombre_mes}_{año_actual}.csv")
                ruta_cierres = os.path.join("Resultado", f"cierres_mes_{nombre_mes}_{año_actual}.csv")
            
            # # Debug prints
            # st.write(f"🔍 Buscando archivos para mes: {mes_seleccionado} ({mes_numero})")
            # st.write("📂 Archivo de aperturas buscado:", ruta_aperturas)
            # st.write("📂 Archivo de cierres buscado:", ruta_cierres)

            # Verificar si los archivos existen
            if not os.path.exists(ruta_aperturas) or not os.path.exists(ruta_cierres):
                st.warning(f"⚠️ No se encontraron archivos para el mes {mes_seleccionado}")
                st.stop()

            # Leer los archivos usando las rutas encontradas
            df_base_cierres = pd.read_csv(ruta_cierres)
            df_base_aperturas = pd.read_csv(ruta_aperturas)
            
            # # Debug prints para verificar los DataFrames
            # st.write("📊 Columnas en DataFrame aperturas:", df_base_aperturas.columns.tolist())
            # st.write("📊 Columnas en DataFrame cierres:", df_base_cierres.columns.tolist())
            
            # if not df_base_aperturas.empty:
            #     st.write("Primeras filas de aperturas:")
            #     st.write(df_base_aperturas.head(2))
            
            # if not df_base_cierres.empty:
            #     st.write("Primeras filas de cierres:")
            #     st.write(df_base_cierres.head(2))

            df_base_cierres.rename(columns={'Fuerza_Comercial': 'Aliado'}, inplace=True)
            df_base_aperturas.rename(columns={'Fuerza_Comercial': 'Aliado'}, inplace=True)

            # Mostrar la fecha de última actualización basada en el archivo de aperturas
            ultima_actualizacion = os.path.getmtime(ruta_aperturas)
            fecha_actualizacion = pd.to_datetime(ultima_actualizacion, unit='s').strftime("%d/%m/%Y")
            st.write("🕒 Última actualización:", fecha_actualizacion)

            # Limpiar los dataframes
            df_base_cierres = limpiar_dataframe(df_base_cierres)
            df_base_aperturas = limpiar_dataframe(df_base_aperturas)
            
            # # Debug prints después de la limpieza
            # st.write("📊 Tamaño DataFrame aperturas después de limpieza:", df_base_aperturas.shape)
            # st.write("📊 Tamaño DataFrame cierres después de limpieza:", df_base_cierres.shape)

        except Exception as e:
            st.error(f"❌ Error al cargar archivos: {str(e)}")
            st.write("Detalles del error:", str(e))

        # Función para crear mapa de puntos
        def crear_mapa_puntos(df, titulo):
            # Filtrar por aliado si se seleccionó uno específico
            if opcion_aliado != 'Todos':
                df = df[df['Aliado'] == opcion_aliado]

            if opcion_mapa == 'Todos':
                # Para vista 'Todos', colorear por tipo
                fig = px.scatter_map(
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
                fig = px.scatter_map(
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

    except Exception as e:
        st.error(f"⚠️ Error al leer el archivo: {e}")

    except FileNotFoundError:
        st.error("No se encontró el archivo de informe diario en la carpeta Resultado")
        st.stop()



elif st.session_state.get('authentication_status') == False:
    st.error("❌ Usuario o contraseña incorrectos")
elif st.session_state.get('authentication_status') is None:
    st.warning("🔑 Por favor inicia sesión")

