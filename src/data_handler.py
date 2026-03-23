import os
import csv
import pandas as pd
import streamlit as st
from datetime import datetime
from src.constants import (
    DATA_DIR, DATA_FILE, LIKERT_TO_NUM,
    ASPECTOS_EVENTO, GENEROS_MUSICALES, SERVICIOS_MESA
)

CSV_COLUMNS = (
    ["nombre_completo", "carrera", "matricula", "telefono",
     "presupuesto", "mesas_12", "mesas_10",
     "num_boletos", "asignacion_boletos", "compañero_descripcion",
     "lugar_preferido", "lugar_otro"]
    + list(SERVICIOS_MESA.keys())
    + list(ASPECTOS_EVENTO.keys())
    + list(GENEROS_MUSICALES.keys())
    + ["alergias", "mes_preferido", "comentarios", "fecha_registro"]
)


def _asegurar_directorio():
    os.makedirs(DATA_DIR, exist_ok=True)


def guardar_registro(datos):
    _asegurar_directorio()

    # Convertir etiquetas Likert a valores numéricos (1-5)
    for key in list(ASPECTOS_EVENTO) + list(GENEROS_MUSICALES):
        if key in datos and isinstance(datos[key], str):
            datos[key] = LIKERT_TO_NUM.get(datos[key], 3)

    datos["fecha_registro"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    archivo_existe = os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        if not archivo_existe:
            writer.writeheader()
        writer.writerow({col: datos.get(col, "") for col in CSV_COLUMNS})

    with st.expander("Ver resumen de tu registro"):
        st.write(f"**Nombre:** {datos.get('nombre_completo')}")
        st.write(f"**Carrera:** {datos.get('carrera')}")
        st.write(f"**Matrícula:** {datos.get('matricula')}")
        st.write(f"**Teléfono:** {datos.get('telefono')}")
        st.write(f"**Presupuesto por persona:** {datos.get('presupuesto')}")
        st.write(f"**Mesas (escenario 12p):** {datos.get('mesas_12')}")
        st.write(f"**Mesas (escenario 10p):** {datos.get('mesas_10')}")
        st.write(f"**Boletos individuales:** {datos.get('num_boletos')}")
        st.write(f"**Acomodo:** {datos.get('asignacion_boletos')}")
        st.write(f"**Lugar preferido:** {datos.get('lugar_preferido')}")
        if datos.get("lugar_otro"):
            st.write(f"**Lugar propuesto:** {datos.get('lugar_otro')}")
        if datos.get("alergias"):
            st.write(f"**Alergias:** {datos['alergias']}")
        if datos.get("comentarios"):
            st.write(f"**Sugerencias:** {datos['comentarios']}")


def ya_registro(matricula="", nombre=""):
    """Devuelve True si la matrícula o el nombre ya existe en el CSV."""
    if not os.path.exists(DATA_FILE):
        return False
    df = pd.read_csv(DATA_FILE, encoding="utf-8", dtype=str)
    if matricula:
        if (df["matricula"].str.strip() == matricula.strip()).any():
            return True
    if nombre:
        if (df["nombre_completo"].str.strip().str.lower() == nombre.strip().lower()).any():
            return True
    return False


def cargar_registros():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=CSV_COLUMNS)
    return pd.read_csv(DATA_FILE, encoding="utf-8")


def obtener_csv_bytes():
    df = cargar_registros()
    return df.to_csv(index=False).encode("utf-8")
