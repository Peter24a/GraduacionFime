import streamlit as st
from src.constants import (
    CARRERAS, OPCIONES_PAGO, LUGARES_EVENTO, MESES_PREFERIDOS,
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
    matricula = st.text_input(
        "Número de Cuenta *", placeholder="Ej. 2018xxxx"
    )
    carrera = st.selectbox("Carrera *", CARRERAS)
    telefono = st.text_input(
        "Teléfono de contacto (WhatsApp)", placeholder="10 dígitos"
    )
    return {
        "nombre_completo": nombre_completo,
        "carrera": carrera,
        "matricula": matricula,
        "telefono": telefono,
    }


def render_lugar_evento():
    """Llamar ANTES del form para habilitar campo 'Otro'."""
    st.markdown("---")
    st.markdown("### Lugar del Evento")
    lugar = st.radio(
        "¿Cuál sería tu lugar preferido para la graduación?",
        LUGARES_EVENTO,
        key="lugar_radio",
    )
    lugar_otro = ""
    if lugar == "Otro":
        lugar_otro = st.text_input(
            "¿Qué lugar propones?",
            placeholder="Nombre del lugar y por qué lo recomiendas",
            key="lugar_otro_input",
        )
    return lugar, lugar_otro


def render_detalles_evento(lugar_preferido, lugar_otro, escenario_c):
    st.markdown("---")
    st.markdown("### Detalles de la Fiesta de Graduación")

    pago_dispuesto = st.selectbox(
        "¿Cuánto estás dispuesto a pagar por persona? (Aproximado)",
        OPCIONES_PAGO,
    )

    mesas_12, mesas_10 = 0, 0
    num_boletos, asignacion_boletos, compañero_descripcion = 0, "", ""

    if escenario_c:
        # --- Escenario C: Boleto individual ---
        st.markdown("---")
        st.markdown("### Escenario C — Boleto individual")
        st.warning(
            "📋 Deberás comunicarte con el comité organizador para coordinar la asignación."
        )
        num_boletos = st.number_input(
            "¿Cuántos boletos individuales necesitas?",
            min_value=1, max_value=20, value=1, step=1,
            key="num_boletos",
        )
        asignacion_boletos = st.radio(
            "¿Cómo prefieres que sea tu acomodo?",
            ["Aleatorio", "Con alguien específico"],
            key="asignacion_radio",
        )
        compañero_descripcion = st.text_input(
            "Si elegiste 'Con alguien específico', ¿con quién te gustaría sentarte?",
            placeholder="Ej. amigos de mi grupo, compañeros de la misma materia, etc.",
            key="compañero_input",
        )
    else:
        # --- Escenario A: Mesa de 12 personas ---
        st.markdown("---")
        st.markdown("### Escenario A — Mesa de 12 personas")
        st.info("Si las mesas son de **12 personas**, ¿cuántas necesitarías?")
        mesas_12 = st.number_input(
            "Número de mesas (12 personas c/u)",
            min_value=1, max_value=10, value=1, step=1,
            key="mesas_12",
        )

        # --- Escenario B: Mesa de 10 personas ---
        st.markdown("### Escenario B — Mesa de 10 personas")
        st.info("Si las mesas son de **10 personas**, ¿cuántas necesitarías?")
        mesas_10 = st.number_input(
            "Número de mesas (10 personas c/u)",
            min_value=1, max_value=10, value=1, step=1,
            key="mesas_10",
        )

    # --- Servicios de mesa ---
    st.markdown("---")
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
        "mesas_12": mesas_12,
        "mesas_10": mesas_10,
        "num_boletos": num_boletos,
        "asignacion_boletos": asignacion_boletos,
        "compañero_descripcion": compañero_descripcion,
        "lugar_preferido": lugar_preferido,
        "lugar_otro": lugar_otro,
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
    mes_preferido = st.selectbox(
        "¿En qué mes preferirías que se realizara el evento?",
        MESES_PREFERIDOS,
    )
    alergias = st.text_input(
        "Alergias o preferencias de comida (opcional)",
        placeholder="Ej. Vegano, alergia al maní, etc.",
    )
    comentarios = st.text_area(
        "¿Qué más consideras necesario para el evento?",
        placeholder="Tus sugerencias nos ayudan a mejorar el evento...",
    )
    st.markdown("*Los campos marcados con (*) son obligatorios.*")
    return {"mes_preferido": mes_preferido, "alergias": alergias, "comentarios": comentarios}
