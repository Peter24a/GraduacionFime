import streamlit as st
from src.constants import (
    CARRERAS, OPCIONES_PAGO, PERSONAS_POR_MESA,
    LIKERT_OPTIONS, ASPECTOS_EVENTO, GENEROS_MUSICALES,
    SERVICIOS_MESA
)


def configurar_pagina():
    st.set_page_config(
        page_title="Registro Graduación FIME",
        page_icon="🎓",
        layout="centered"
    )
    st.markdown("""
        <style>
        .main { background-color: #f8f9fa; }
        h1 { color: #2c3e50; }
        </style>
    """, unsafe_allow_html=True)


def mostrar_encabezado():
    st.title("🎓 Registro de Graduación FIME")
    st.write(
        "¡Felicidades por estar a un paso de graduarte! "
        "Por favor, llena el siguiente formulario para ayudarnos "
        "a organizar el mejor evento posible."
    )


def render_informacion_personal():
    st.markdown("### Información Personal")
    nombre_completo = st.text_input(
        "Nombre Completo *", placeholder="Ingresa tu nombre y apellidos"
    )
    carrera = st.selectbox("Carrera *", CARRERAS)
    matricula = st.text_input(
        "Número de Cuenta / Matrícula", placeholder="Ej. 2018xxxx"
    )
    telefono = st.text_input(
        "Teléfono de contacto (WhatsApp)", placeholder="10 dígitos"
    )
    return {
        "nombre_completo": nombre_completo,
        "carrera": carrera,
        "matricula": matricula,
        "telefono": telefono,
    }


def render_detalles_evento():
    st.markdown("---")
    st.markdown("### Detalles de la Fiesta de Graduación")

    pago_dispuesto = st.selectbox(
        "¿Cuánto estás dispuesto a pagar por tu paquete de graduación? (Aproximado)",
        OPCIONES_PAGO,
    )

    # --- Mesas e invitados ---
    st.markdown("---")
    st.markdown("### Mesas e Invitados")
    st.info(
        f"Cada mesa tiene capacidad para **{PERSONAS_POR_MESA} personas**. "
        "Considera esto al calcular cuántas mesas necesitas."
    )

    col1, col2 = st.columns(2)
    with col1:
        invitados = st.number_input(
            "¿Cuántas personas llevarás? (contándote a ti)",
            min_value=1, max_value=100, value=5, step=1,
        )
    with col2:
        mesas = st.number_input(
            f"¿Cuántas mesas necesitarás? ({PERSONAS_POR_MESA} personas c/u)",
            min_value=1, max_value=10, value=1, step=1,
        )

    st.markdown("**¿Qué servicios te gustaría en tu mesa?**")
    servicios_sel = st.multiselect(
        "Selecciona los servicios deseados",
        options=list(SERVICIOS_MESA.values()),
        default=[],
    )
    servicios_dict = {
        col_key: (1 if label in servicios_sel else 0)
        for col_key, label in SERVICIOS_MESA.items()
    }

    return {
        "presupuesto": pago_dispuesto,
        "invitados": invitados,
        "mesas": mesas,
        **servicios_dict,
    }


def render_likert_evento():
    st.markdown("---")
    st.markdown("### ¿Qué tan importante es para ti cada aspecto del evento?")
    st.caption("Califica de «Nada importante» a «Muy importante».")

    datos = {}
    for col_key, label in ASPECTOS_EVENTO.items():
        datos[col_key] = st.select_slider(
            label, options=LIKERT_OPTIONS, value="Neutral", key=col_key,
        )
    return datos


def render_likert_musica():
    st.markdown("---")
    st.markdown("### ¿Qué géneros musicales prefieres para el evento?")
    st.caption("Califica de «Nada importante» a «Muy importante».")

    datos = {}
    for col_key, label in GENEROS_MUSICALES.items():
        datos[col_key] = st.select_slider(
            label, options=LIKERT_OPTIONS, value="Neutral", key=col_key,
        )
    return datos


def render_preferencias():
    st.markdown("---")
    st.markdown("### Preferencias Adicionales")
    alergias = st.text_input(
        "Alergias o preferencias de comida (opcional)",
        placeholder="Ej. Vegano, alergia al maní, etc.",
    )
    comentarios = st.text_area(
        "¿Qué más consideras necesario para el evento?",
        placeholder="Tus sugerencias nos ayudan a mejorar el evento...",
    )
    st.markdown("*Los campos marcados con (*) son obligatorios.*")
    return {"alergias": alergias, "comentarios": comentarios}
