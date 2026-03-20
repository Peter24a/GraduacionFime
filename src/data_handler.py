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
     "presupuesto", "invitados", "mesas"]
    + list(SERVICIOS_MESA.keys())
    + list(ASPECTOS_EVENTO.keys())
    + list(GENEROS_MUSICALES.keys())
    + ["alergias", "comentarios", "fecha_registro"]
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
        st.write(f"**Presupuesto:** {datos.get('presupuesto')}")
        st.write(f"**Invitados:** {datos.get('invitados')}")
        st.write(f"**Mesas:** {datos.get('mesas')}")
        if datos.get("alergias"):
            st.write(f"**Alergias:** {datos['alergias']}")
        if datos.get("comentarios"):
            st.write(f"**Sugerencias:** {datos['comentarios']}")


def cargar_registros():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=CSV_COLUMNS)
    return pd.read_csv(DATA_FILE, encoding="utf-8")


def obtener_csv_bytes():
    df = cargar_registros()
    return df.to_csv(index=False).encode("utf-8")
