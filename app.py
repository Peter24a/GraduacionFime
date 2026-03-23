import streamlit as st
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
from src.data_handler import guardar_registro, ya_registro
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
    mostrar_encabezado()

    # Selecciones fuera del form (renderizado condicional)
    lugar_preferido, lugar_otro = render_lugar_evento()

    st.markdown("---")
    escenario_c = st.checkbox(
        "También quiero indicar mi preferencia para boleto individual (Escenario C)"
    )

    with st.form("registro_graduacion_form", enter_to_submit=False):
        datos_personales = render_informacion_personal()
        datos_evento = render_detalles_evento(lugar_preferido, lugar_otro, escenario_c)
        datos_likert = render_likert_evento()
        datos_musica = render_likert_musica()
        datos_preferencias = render_preferencias()
        enviado = st.form_submit_button("Registrar mis datos")

    if enviado:
        if not datos_personales["nombre_completo"]:
            st.error("Por favor, ingresa tu nombre completo.")
        elif ya_registro(
            matricula=datos_personales.get("matricula", ""),
            nombre=datos_personales.get("nombre_completo", ""),
        ):
            st.warning(
                "Ya existe un registro con ese número de cuenta o nombre. "
                "Si necesitas modificar tu registro, contacta al comité organizador."
            )
        else:
            datos_finales = {
                **datos_personales,
                **datos_evento,
                **datos_likert,
                **datos_musica,
                **datos_preferencias,
            }
            guardar_registro(datos_finales)

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
