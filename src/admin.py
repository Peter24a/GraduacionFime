import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.constants import (
    ADMIN_PASSWORD, ASPECTOS_EVENTO, GENEROS_MUSICALES,
    SERVICIOS_MESA, NUM_TO_LIKERT
)
from src.data_handler import cargar_registros, obtener_csv_bytes


def render_admin():
    st.title("Panel de Administración")

    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        password = st.text_input("Contraseña de administrador", type="password")
        if st.button("Ingresar"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
        return

    st.success("Sesión de administrador activa")
    if st.button("Cerrar sesión"):
        st.session_state.admin_auth = False
        st.rerun()

    df = cargar_registros()

    if df.empty:
        st.warning("No hay registros aún.")
        return

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Resumen General",
        "Evento y Música",
        "Mesas y Servicios",
        "EDA",
        "Datos Completos",
    ])

    with tab1:
        _render_resumen(df)
    with tab2:
        _render_evento_musica(df)
    with tab3:
        _render_mesas(df)
    with tab4:
        _render_eda(df)
    with tab5:
        _render_datos(df)


# ── Tab 1: Resumen ──────────────────────────────────────────────────────────

def _render_resumen(df):
    st.markdown("### Métricas Generales")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Registros", len(df))
    with c2:
        st.metric("Invitados", int(df["invitados"].sum()) if "invitados" in df.columns else 0)
    with c3:
        st.metric("Mesas", int(df["mesas"].sum()) if "mesas" in df.columns else 0)
    with c4:
        capacidad = int(df["invitados"].sum()) if "invitados" in df.columns else 0
        st.metric("Total invitados", capacidad)

    col_l, col_r = st.columns(2)

    with col_l:
        if "carrera" in df.columns:
            st.markdown("#### Registros por Carrera")
            counts = df["carrera"].value_counts().reset_index()
            counts.columns = ["Carrera", "Registros"]
            fig = px.pie(counts, values="Registros", names="Carrera", hole=0.4)
            fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=350)
            st.plotly_chart(fig, use_container_width=True)

    with col_r:
        if "presupuesto" in df.columns:
            st.markdown("#### Presupuesto Dispuesto")
            counts = df["presupuesto"].value_counts().reset_index()
            counts.columns = ["Presupuesto", "Registros"]
            fig = px.bar(counts, x="Presupuesto", y="Registros", color="Presupuesto")
            fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10), height=350, showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

    # Registros en el tiempo
    if "fecha_registro" in df.columns:
        st.markdown("#### Registros a lo Largo del Tiempo")
        df_time = df.copy()
        df_time["fecha"] = pd.to_datetime(df_time["fecha_registro"]).dt.date
        by_date = df_time.groupby("fecha").size().reset_index(name="Registros")
        fig = px.line(by_date, x="fecha", y="Registros", markers=True)
        fig.update_layout(
            xaxis_title="Fecha", yaxis_title="Registros",
            margin=dict(t=10, b=10), height=280,
        )
        st.plotly_chart(fig, use_container_width=True)


# ── Tab 2: Evento y Música ──────────────────────────────────────────────────

def _render_evento_musica(df):
    # ── Aspectos del evento ──
    likert_cols = [c for c in ASPECTOS_EVENTO if c in df.columns]
    if likert_cols:
        st.markdown("### Importancia de Aspectos del Evento")
        st.caption("Promedio en escala 1‑5 (1 = Nada importante · 5 = Muy importante)")

        means = (
            df[likert_cols]
            .apply(pd.to_numeric, errors="coerce")
            .mean()
            .dropna()
            .sort_values(ascending=True)
        )
        labels = [ASPECTOS_EVENTO[c] for c in means.index]

        fig = px.bar(
            x=means.values, y=labels, orientation="h",
            color=means.values, color_continuous_scale="RdYlGn", range_color=[1, 5],
        )
        fig.update_layout(
            xaxis_title="Promedio", yaxis_title="",
            coloraxis_colorbar_title="Puntaje",
            margin=dict(t=10, b=10), height=420,
        )
        fig.update_xaxes(range=[0, 5.5])
        st.plotly_chart(fig, use_container_width=True)

        # Heatmap de distribución
        st.markdown("#### Distribución de Respuestas")
        _render_heatmap(df, likert_cols, ASPECTOS_EVENTO, "YlGnBu")

    # ── Géneros musicales ──
    musica_cols = [c for c in GENEROS_MUSICALES if c in df.columns]
    if musica_cols:
        st.markdown("### Preferencias Musicales")
        st.caption("Promedio en escala 1‑5")

        means = (
            df[musica_cols]
            .apply(pd.to_numeric, errors="coerce")
            .mean()
            .dropna()
            .sort_values(ascending=True)
        )
        labels = [GENEROS_MUSICALES[c] for c in means.index]

        fig = px.bar(
            x=means.values, y=labels, orientation="h",
            color=means.values, color_continuous_scale="Purples", range_color=[1, 5],
        )
        fig.update_layout(
            xaxis_title="Promedio", yaxis_title="",
            coloraxis_colorbar_title="Puntaje",
            margin=dict(t=10, b=10), height=420,
        )
        fig.update_xaxes(range=[0, 5.5])
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Distribución de Respuestas Musicales")
        _render_heatmap(df, musica_cols, GENEROS_MUSICALES, "Purples")

    # ── Radar comparativo ──
    if likert_cols and musica_cols:
        st.markdown("### Radar: Top 6 Aspectos vs Top 6 Géneros")
        _render_radar(df, likert_cols, musica_cols)


def _render_heatmap(df, cols, label_map, colorscale):
    rows = []
    for col in cols:
        if col in df.columns:
            counts = (
                df[col]
                .apply(pd.to_numeric, errors="coerce")
                .dropna()
                .astype(int)
                .value_counts()
                .reindex([1, 2, 3, 4, 5], fill_value=0)
            )
            rows.append(counts.values)
    if not rows:
        return
    heatmap_df = pd.DataFrame(
        rows,
        index=[label_map[c] for c in cols if c in df.columns],
        columns=["Nada imp.", "Poco imp.", "Neutral", "Importante", "Muy imp."],
    )
    fig = px.imshow(heatmap_df, color_continuous_scale=colorscale,
                    aspect="auto", text_auto=True)
    fig.update_layout(margin=dict(t=10, b=10), height=max(250, len(rows) * 38))
    st.plotly_chart(fig, use_container_width=True)


def _render_radar(df, likert_cols, musica_cols):
    ev_means = (
        df[likert_cols].apply(pd.to_numeric, errors="coerce").mean().dropna()
        .nlargest(6)
    )
    mu_means = (
        df[musica_cols].apply(pd.to_numeric, errors="coerce").mean().dropna()
        .nlargest(6)
    )
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(ev_means.values) + [ev_means.values[0]],
        theta=[ASPECTOS_EVENTO[c] for c in ev_means.index] + [ASPECTOS_EVENTO[ev_means.index[0]]],
        fill="toself", name="Evento",
    ))
    fig.add_trace(go.Scatterpolar(
        r=list(mu_means.values) + [mu_means.values[0]],
        theta=[GENEROS_MUSICALES[c] for c in mu_means.index] + [GENEROS_MUSICALES[mu_means.index[0]]],
        fill="toself", name="Música",
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        margin=dict(t=30, b=30), height=420, showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Tab 3: Mesas y Servicios ────────────────────────────────────────────────

def _render_mesas(df):
    st.markdown("### Estadísticas de Mesas y Servicios")

    if "mesas" in df.columns and "invitados" in df.columns:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Prom. invitados/registro", f"{df['invitados'].mean():.1f}")
        with c2:
            st.metric("Prom. mesas/registro", f"{df['mesas'].mean():.1f}")
        with c3:
            st.metric("Total mesas", int(df["mesas"].sum()))

    # Servicios de mesa
    mesa_cols = [c for c in SERVICIOS_MESA if c in df.columns]
    if mesa_cols:
        st.markdown("#### Servicios de Mesa Más Solicitados")
        pct = (
            df[mesa_cols]
            .apply(pd.to_numeric, errors="coerce")
            .sum() / len(df) * 100
        ).sort_values(ascending=True)
        labels = [SERVICIOS_MESA[c] for c in pct.index]

        fig = px.bar(
            x=pct.values, y=labels, orientation="h",
            color=pct.values, color_continuous_scale="Teal",
            text=[f"{v:.0f}%" for v in pct.values],
        )
        fig.update_layout(
            xaxis_title="% de registros", yaxis_title="",
            margin=dict(t=10, b=10), height=300, showlegend=False,
        )
        fig.update_xaxes(range=[0, 105])
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    # Distribución de invitados
    if "invitados" in df.columns:
        st.markdown("#### Distribución de Invitados por Registro")
        fig = px.histogram(
            df, x="invitados", nbins=15,
            color_discrete_sequence=["#2c3e50"],
        )
        fig.update_layout(
            xaxis_title="Número de invitados", yaxis_title="Frecuencia",
            margin=dict(t=10, b=10), height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Distribución de mesas
    if "mesas" in df.columns:
        st.markdown("#### Distribución de Mesas por Registro")
        fig = px.histogram(
            df, x="mesas", nbins=10,
            color_discrete_sequence=["#16a085"],
        )
        fig.update_layout(
            xaxis_title="Mesas solicitadas", yaxis_title="Frecuencia",
            margin=dict(t=10, b=10), height=300,
        )
        st.plotly_chart(fig, use_container_width=True)


# ── Tab 4: EDA ──────────────────────────────────────────────────────────────

def _render_eda(df):
    st.markdown("## Análisis Exploratorio de Datos")

    num_cols = df.select_dtypes(include="number").columns.tolist()
    df_num = df[num_cols].apply(pd.to_numeric, errors="coerce")

    # ── Estadísticas descriptivas ──
    st.markdown("### Estadísticas Descriptivas")
    st.dataframe(df_num.describe().round(2), use_container_width=True)

    st.markdown("---")

    # ── Presupuesto vs Carrera ──
    if {"presupuesto", "carrera"}.issubset(df.columns):
        st.markdown("### Presupuesto por Carrera")
        cross = (
            df.groupby(["carrera", "presupuesto"])
            .size()
            .reset_index(name="count")
        )
        fig = px.bar(
            cross, x="carrera", y="count", color="presupuesto",
            barmode="stack", labels={"carrera": "Carrera", "count": "Registros"},
        )
        fig.update_layout(margin=dict(t=10, b=80), height=380, xaxis_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)

    # ── Lugar preferido ──
    if "lugar_preferido" in df.columns:
        st.markdown("### Lugar Preferido")
        counts = df["lugar_preferido"].value_counts().reset_index()
        counts.columns = ["Lugar", "Registros"]
        col_l, col_r = st.columns(2)
        with col_l:
            fig = px.pie(counts, values="Registros", names="Lugar", hole=0.4)
            fig.update_layout(margin=dict(t=10, b=10), height=300)
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            fig = px.bar(counts, x="Lugar", y="Registros", color="Lugar")
            fig.update_layout(margin=dict(t=10, b=10), height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    # ── Mes preferido ──
    if "mes_preferido" in df.columns:
        st.markdown("### Mes Preferido")
        counts = df["mes_preferido"].value_counts().reset_index()
        counts.columns = ["Mes", "Registros"]
        fig = px.bar(counts, x="Mes", y="Registros", color="Mes",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(margin=dict(t=10, b=10), height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Mesas 12 vs Mesas 10 ──
    if {"mesas_12", "mesas_10"}.issubset(df.columns):
        st.markdown("### Mesas: Escenario A (12p) vs Escenario B (10p)")
        df_mesas = df[["mesas_12", "mesas_10"]].apply(pd.to_numeric, errors="coerce").dropna()
        df_mesas = df_mesas[df_mesas[["mesas_12", "mesas_10"]].gt(0).any(axis=1)]
        col_l, col_r = st.columns(2)
        with col_l:
            fig = px.histogram(df_mesas, x="mesas_12", nbins=10, title="Escenario A — 12p",
                               color_discrete_sequence=["#2980b9"])
            fig.update_layout(margin=dict(t=30, b=10), height=280)
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            fig = px.histogram(df_mesas, x="mesas_10", nbins=10, title="Escenario B — 10p",
                               color_discrete_sequence=["#27ae60"])
            fig.update_layout(margin=dict(t=30, b=10), height=280)
            st.plotly_chart(fig, use_container_width=True)

        if len(df_mesas) > 1:
            st.markdown("#### Correlación A vs B")
            fig = px.scatter(df_mesas, x="mesas_12", y="mesas_10",
                             opacity=0.7,
                             labels={"mesas_12": "Mesas (12p)", "mesas_10": "Mesas (10p)"})
            fig.update_layout(margin=dict(t=10, b=10), height=320)
            st.plotly_chart(fig, use_container_width=True)

    # ── Boletos individuales ──
    if "num_boletos" in df.columns:
        df_c = df[pd.to_numeric(df["num_boletos"], errors="coerce").gt(0)]
        if not df_c.empty:
            st.markdown("### Escenario C — Boletos Individuales")
            col_l, col_r = st.columns(2)
            with col_l:
                fig = px.histogram(df_c, x=pd.to_numeric(df_c["num_boletos"], errors="coerce"),
                                   nbins=10, color_discrete_sequence=["#e67e22"])
                fig.update_layout(xaxis_title="Boletos", yaxis_title="Frecuencia",
                                  margin=dict(t=10, b=10), height=280)
                st.plotly_chart(fig, use_container_width=True)
            with col_r:
                if "asignacion_boletos" in df_c.columns:
                    counts = df_c["asignacion_boletos"].value_counts().reset_index()
                    counts.columns = ["Tipo", "Registros"]
                    fig = px.pie(counts, values="Registros", names="Tipo", hole=0.4)
                    fig.update_layout(margin=dict(t=10, b=10), height=280)
                    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Matriz de correlación ──
    if len(df_num.columns) > 1:
        st.markdown("### Matriz de Correlación (variables numéricas)")
        corr = df_num.corr().round(2)
        fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                        zmin=-1, zmax=1, aspect="auto")
        fig.update_layout(margin=dict(t=10, b=10), height=max(400, len(corr) * 30))
        st.plotly_chart(fig, use_container_width=True)

    # ── Boxplots Likert por carrera ──
    likert_cols = [c for c in ASPECTOS_EVENTO if c in df.columns]
    if likert_cols and "carrera" in df.columns:
        st.markdown("### Distribución Likert por Carrera")
        aspecto = st.selectbox(
            "Selecciona un aspecto:", [ASPECTOS_EVENTO[c] for c in likert_cols],
            key="eda_aspecto"
        )
        col_key = [k for k, v in ASPECTOS_EVENTO.items() if v == aspecto][0]
        df_box = df[["carrera", col_key]].copy()
        df_box[col_key] = pd.to_numeric(df_box[col_key], errors="coerce")
        fig = px.box(df_box, x="carrera", y=col_key, color="carrera",
                     labels={"carrera": "Carrera", col_key: "Puntaje (1-5)"},
                     points="all")
        fig.update_layout(margin=dict(t=10, b=60), height=380,
                          xaxis_tickangle=-30, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


# ── Tab 5: Datos Completos ──────────────────────────────────────────────────

def _render_datos(df):
    st.markdown("### Todos los Registros")

    # Filtro por carrera
    if "carrera" in df.columns:
        opciones = ["Todas"] + sorted(df["carrera"].unique().tolist())
        filtro = st.selectbox("Filtrar por carrera:", opciones)
        if filtro != "Todas":
            df = df[df["carrera"] == filtro]

    st.dataframe(df, use_container_width=True, height=420)
    st.caption(f"Mostrando **{len(df)}** registro(s)")

    st.download_button(
        label="Descargar CSV completo",
        data=obtener_csv_bytes(),
        file_name="registros_graduacion_fime.csv",
        mime="text/csv",
    )
