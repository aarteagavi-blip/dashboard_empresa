# GRÁFICOS DE BARRAS EN STREAMLIT:
# --------------------------------



import plotly.express as px


# GRÁFICO 1


def grafico_ventas(df):

    ventas = df.groupby("marca")["cantidad"].sum().reset_index()

    grafico01 = px.bar(
        ventas,
        x="marca",
        y="cantidad",
        #title="🚗 Ventas por Marca",
        text_auto=True,
        color="cantidad",
        color_continuous_scale="Blues"
    )

    grafico01.update_layout(

        #title_x=0.5,

        title={
                "text": "🚗 Ventas por Marca",
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
        title_xanchor="center",

        plot_bgcolor="white",

        paper_bgcolor="white",

        xaxis_title="Marca",

        yaxis_title="Cantidad Vendida",

        font=dict(size=15),

        coloraxis_showscale=False

    )

    grafico01.update_traces(

        textposition="outside",

        marker_line_color="black",

        marker_line_width=1

    )

    return grafico01




# GRÁFICO 2
def grafico_promedio(df):

    promedio = df.groupby("marca")["precio_venta"].mean().reset_index()

    grafico02 = px.bar(

        promedio,

        x="marca",

        y="precio_venta",

        #title="💰 Precio Promedio por Marca",

        text_auto=".2f",

        color="precio_venta",

        color_continuous_scale="Teal"

    )

    grafico02.update_layout(

        #title_x=0.5,

        title={
                "text": "💰 Precio Promedio por Marca",
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
        title_xanchor="center",

        plot_bgcolor="white",

        paper_bgcolor="white",

        xaxis_title="Marca",

        yaxis_title="Precio Promedio",

        font=dict(size=15),

        coloraxis_showscale=False

    )

    grafico02.update_traces(

        textposition="outside",

        marker_line_color="black",

        marker_line_width=1

    )

    return grafico02


def grafico_participacion(df):

    ventas = (
        df.groupby("marca")["cantidad"]
        .sum()
        .reset_index()
    )

    grafico03 = px.pie(
        ventas,
        names="marca",
        values="cantidad",
        hole=0.55,
        #title="📊 Participación de Ventas por Marca"
    )

    grafico03.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    grafico03.update_layout(
    title={
        "text": "📊 Participación de Ventas por Marca",
        "x": 0.5,
        "xanchor": "center",
        "yanchor": "top",
    }
)

    return grafico03