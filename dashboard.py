
import streamlit as st

# -------------------------
# Control de sesión
# -------------------------

if "logueado" not in st.session_state:
    st.session_state.logueado = False

st.set_page_config(
    page_title="Wigo Motors",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

from conexion import cargar_datos
from indicadores import *
from graficos import *



# ==========================
# LOGIN
# ==========================

if not st.session_state.logueado:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.image("images.png", width=180)

        st.title("🚗 WIGO MOTORS S.A.C.")

        st.write("### Inicio de Sesión")

        st.caption("Ingrese sus credenciales para acceder...")

        usuario = st.text_input("👤 Usuario")

        contraseña = st.text_input(
            "🔒 Contraseña",
            type="password"
        )

        if st.button(
            "Ingresar",
            use_container_width=True
        ):

            if usuario == "infouni" and contraseña == "12345":

                st.session_state.logueado = True
                st.success("Ingreso correcto")
                st.rerun()

            else:

                st.error("Usuario o contraseña incorrectos.")

    st.stop()

with st.spinner("Conectando con la base de datos..."):
    df = cargar_datos()

st.markdown("""
<style>

/* Fondo principal con imagen */
.stApp{
    background-image: url("https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=1400");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Mantener fijo el ancho del Sidebar */
section[data-testid="stSidebar"]{
    min-width:320px !important;
    max-width:320px !important;
}

/* Títulos */
h1{
    color:#003366;
    font-weight:bold;
}

/* Tarjetas con opacidad */
[data-testid="stMetric"]{
    background-color: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid #E5E5E5;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.10);
}

/* Sidebar */
[data-testid="stSidebar"]{
    background-color:#002B5B;
}

/* Texto del Sidebar */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p{
    color:white;
}

</style>
""", unsafe_allow_html=True)

hide_streamlit = """
<style>

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

</style>
"""

st.markdown(hide_streamlit, unsafe_allow_html=True)


col1,col2 = st.columns([1,5])

with col1:
    st.image("images.png", width=120)

with col2:
    st.title("WIGO MOTORS S.A.C. 🚗")
    st.caption("Comercial de Ventas")


st.divider()

# ============================
# FILTROS DEL DASHBOARD
# ============================

st.sidebar.header("🔎 Filtros del Dashboard")

# Copia del DataFrame original
df_filtrado = df.copy()

# Filtro por Marca
marca = st.sidebar.selectbox(
    "Marca",
    ["Todas"] + sorted(df["marca"].unique().tolist())
)

# Filtro por Asesor
asesor = st.sidebar.selectbox(
    "Asesor Comercial",
    ["Todos"] + sorted(df["asesor_comercial"].unique().tolist())
)

# Filtro por Sede
sede = st.sidebar.selectbox(
    "Sede",
    ["Todas"] + sorted(df["tienda"].unique().tolist())
)

# Aplicar filtros

if marca != "Todas":
    df_filtrado = df_filtrado[df_filtrado["marca"] == marca]

if asesor != "Todos":
    df_filtrado = df_filtrado[df_filtrado["asesor_comercial"] == asesor]

if sede != "Todas":
    df_filtrado = df_filtrado[df_filtrado["tienda"] == sede]

minimo = int(df_filtrado["precio_venta"].min())
maximo = int(df_filtrado["precio_venta"].max())

rango = st.sidebar.slider(
    "💰 Rango de precio",
    min_value=minimo,
    max_value=maximo,
    value=(minimo, maximo)
)

df_filtrado = df_filtrado[
    (df_filtrado["precio_venta"] >= rango[0]) &
    (df_filtrado["precio_venta"] <= rango[1])
]

# INDICADORES GENERALES: 

st.subheader("Indicadores:")

c1, c2, c3, c4 = st.columns(4)        

c1.metric("💰 Precio Total", f"S/{precio_total(df_filtrado):,.2f}")          
c2.metric("🚗 Unidades vendidas", f"{unidades_vendidas(df_filtrado)}")                
c3.metric("📊 Precio promedio", f"S/{precio_promedio(df_filtrado):,.2f}")     
c4.metric("📋 Operaciones", operaciones(df_filtrado))                                      



c5, c6 = st.columns(2)  

c5.metric("⬆️ Precio más alto", f"S/{precio_maximo(df_filtrado):,.2f}")
c6.metric("⬇️ Precio más bajo", f"S/{precio_minimo(df_filtrado):,.2f}")

st.divider()

st.subheader("📄 Resumen Ejecutivo")

if not df_filtrado.empty:

    marca_top = (
        df_filtrado.groupby("marca")["cantidad"]
        .sum()
        .idxmax()
    )

else:

    marca_top = "Sin datos"
st.info(
    f"""
    Durante el análisis se registraron **{operaciones(df_filtrado)} operaciones**,
    con una venta total de **S/ {precio_total(df_filtrado):,.2f}**.
    La marca con mayor cantidad de unidades vendidas es **{marca_top}**,
    con un precio promedio de **S/ {precio_promedio(df_filtrado):,.2f}**.
    """
)

st.divider()

if df_filtrado.empty:

    st.warning("⚠️ No existen registros para los filtros seleccionados.")
    st.stop()

# GRÁFICOS - DASHBOARD 

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        grafico_ventas(df_filtrado),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        grafico_promedio(df_filtrado),
        use_container_width=True
    )

st.plotly_chart(
    grafico_participacion(df_filtrado),
    use_container_width=True
)

st.divider()

st.success(f"Registros encontrados: {len(df_filtrado)}")
st.dataframe(
    df_filtrado,
    use_container_width=True,
    hide_index=True
)

csv = df_filtrado.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Descargar Reporte CSV",
    data=csv,
    file_name="ventas_filtradas.csv",
    mime="text/csv"
)

st.divider()

st.markdown(
    """
    <center>
    <h5>🚗 © 2026 Wigo Motors S.A.C.</h5>
    Dashboard desarrollado con Python • Streamlit • Plotly • MySQL
    </center>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

if st.sidebar.button("🚪 Cerrar sesión"):
    st.session_state.logueado = False
    st.rerun()