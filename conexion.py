import pandas as pd
import mysql.connector

def cargar_datos():

    try:
        conexion_db = mysql.connector.connect(
            host="sql10.freesqldatabase.com",
            user="sql10833735",
            password="9UeFiiSCXD",
            database="sql10833735"
        )

        consulta_sql = "SELECT * FROM ventas_vehiculos" # Consulta de toda la tabla de la DB
        df = pd.read_sql(consulta_sql, conexion_db)     # Creando el DataFrame basado en la tabla
        conexion_db.close()

        return df

    except Exception as error:
        print(f"SE ENCONTRÓ UN PROBLEMA: {error}")
