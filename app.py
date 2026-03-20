import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from src.constants import COOKIE_NAME
from src.ui import (
    configurar_pagina,
    mostrar_encabezado,
    render_informacion_personal,
    render_detalles_evento,
    render_likert_evento,
    render_likert_musica,
    render_preferencias,
)
from src.admin import render_admin
from src.data_handler import guardar_registro

# Configuración (debe ser la primera llamada de Streamlit)
configurar_pagina()

# Navegación
st.sidebar.title("Navegación")
pagina = st.sidebar.radio(
    "Ir a:", ["Registro", "Administración"], label_visibility="collapsed"
)

if pagina == "Administración":
    render_admin()
else:
    # Verificar cookie de envío previo
    cookie_value = streamlit_js_eval(
        js_expressions="document.cookie", key="check_cookie"
    )
    already_submitted = bool(cookie_value) and COOKIE_NAME in str(cookie_value)

    # Fallback con session_state para la sesión actual
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False
    already_submitted = already_submitted or st.session_state.form_submitted

    mostrar_encabezado()

    if already_submitted:
        st.info(
            "Ya has registrado tus datos anteriormente. "
            "¡Gracias por tu participación!"
        )
        st.write("Si necesitas modificar tu registro, contacta al comité organizador.")
    else:
        with st.form("registro_graduacion_form"):
            datos_personales = render_informacion_personal()
            datos_evento = render_detalles_evento()
            datos_likert = render_likert_evento()
            datos_musica = render_likert_musica()
            datos_preferencias = render_preferencias()
            enviado = st.form_submit_button("Registrar mis datos")

        if enviado:
            if not datos_personales["nombre_completo"]:
                st.error("Por favor, ingresa tu nombre completo.")
            else:
                datos_finales = {
                    **datos_personales,
                    **datos_evento,
                    **datos_likert,
                    **datos_musica,
                    **datos_preferencias,
                }
                guardar_registro(datos_finales)

                # Cookie en el navegador (1 año)
                streamlit_js_eval(
                    js_expressions=(
                        f"document.cookie = '{COOKIE_NAME}=true; "
                        f"max-age=31536000; path=/'; true"
                    ),
                    key="set_cookie",
                )
                st.session_state.form_submitted = True

                st.success(
                    f"¡Gracias, {datos_personales['nombre_completo']}! "
                    "Tu registro se ha guardado exitosamente."
                )
                st.balloons()
