
import streamlit as st

st.set_page_config(
    page_title="Wigo Motors",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)
from conexion import cargar_datos
from indicadores import *
from graficos import *

df = cargar_datos()

st.title("WIGO MOTORS S.A.C.")  #titulo principal
st.subheader("Buscador comercial")  #sub titulo

st.sidebar.header("Buscador")
tipo_busqueda = st.sidebar.selectbox("Seleccione tipo de búsqueda", ["Marca", "Asesor Comercial", "Sede"])

df_filtrado = df.copy()

#filtro por marca

if tipo_busqueda == "Marca":
    valor = st.sidebar.selectbox("Seleccionar marca", df["marca"].unique()) #mostrar marcas disponibles y sin repetir

    df_filtrado = df[df["marca"] == valor] #filtrar por marca

elif tipo_busqueda == "Asesor Comercial":
    valor = st.sidebar.selectbox("Seleccionar Asesor", df["asesor_comercial"].unique()) #mostrar marcas disponibles y sin repetir

    df_filtrado = df[df["asesor_comercial"] == valor] 

elif tipo_busqueda == "Sede":
    valor = st.sidebar.selectbox("Seleccionar Sede", df["tienda"].unique()) #mostrar marcas disponibles y sin repetir

    df_filtrado = df[df["tienda"] == valor] 


st.success(f"Registros encontrados: {len(df_filtrado)}")
st.dataframe(df_filtrado)


# INDICADORES GENERALES: 

st.subheader("Indicadores:")

c1, c2, c3, c4 = st.columns(4)        

c1.metric("Precio Total", f"S/{precio_total(df_filtrado):,.2f}")          
c2.metric("Unidades vendidas", f"{unidades_vendidas(df_filtrado)}")                
c3.metric("Precio promedio", f"S/{precio_promedio(df_filtrado):,.2f}")     
c4.metric("Operaciones", operaciones(df_filtrado))                                      



c5, c6, c7, c8 = st.columns(4)  

c5.metric("Precio más alto", f"S/{precio_maximo(df_filtrado):,.2f}")
c6.metric("Precio más bajo", f"S/{precio_minimo(df_filtrado):,.2f}")


# GRÁFICOS - DASHBOARD 

st.plotly_chart(grafico_ventas(df_filtrado))  
st.plotly_chart(grafico_promedio(df_filtrado)) 
