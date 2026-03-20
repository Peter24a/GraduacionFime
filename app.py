import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from src.constants import COOKIE_NAME
from src.ui import (
    configurar_pagina,
    mostrar_encabezado,
    render_informacion_personal,
    render_lugar_evento,
    render_detalles_evento,
    render_likert_evento,
    render_likert_musica,
    render_preferencias,
)
from src.admin import render_admin
from src.data_handler import guardar_registro
from src.llm import generar_resumen_graduacion

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
        # Setear cookie de forma lazy (el rerun aquí ya no interrumpe nada)
        cookie_persistida = bool(cookie_value) and COOKIE_NAME in str(cookie_value)
        if not cookie_persistida:
            streamlit_js_eval(
                js_expressions=(
                    f"document.cookie = '{COOKIE_NAME}=true; "
                    f"max-age=31536000; path=/'; true"
                ),
                key="set_cookie",
            )
        st.info(
            "Ya has registrado tus datos anteriormente. "
            "¡Gracias por tu participación!"
        )
        st.write("Si necesitas modificar tu registro, contacta al comité organizador.")
        if st.session_state.get("resumen_llm"):
            st.markdown("---")
            st.markdown("### 🎉 Así podría verse tu graduación")
            st.info(st.session_state.resumen_llm)
    else:
        # Selecciones fuera del form (renderizado condicional)
        lugar_preferido, lugar_otro = render_lugar_evento()

        st.markdown("---")
        escenario_c = st.checkbox(
            "También quiero indicar mi preferencia para boleto individual (Escenario C)"
        )

        with st.form("registro_graduacion_form"):
            datos_personales = render_informacion_personal()
            datos_evento = render_detalles_evento(lugar_preferido, lugar_otro, escenario_c)
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
                st.session_state.form_submitted = True

                st.success(
                    f"¡Gracias, {datos_personales['nombre_completo']}! "
                    "Tu registro se ha guardado exitosamente."
                )
                st.balloons()

                with st.spinner("Generando tu vista previa de graduación..."):
                    st.session_state.resumen_llm = generar_resumen_graduacion(datos_finales)
                st.markdown("---")
                st.markdown("### 🎉 Así podría verse tu graduación")
                st.info(st.session_state.resumen_llm)
