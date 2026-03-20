CARRERAS = [
    "Ingeniería en Computación Inteligente",
    "Ingeniería en Mecatrónica",
    "Ingeniería en Sistemas Electrónicos y Telecomunicaciones",
    "Ingeniero Mecánico Electricista",
    "Otra"
]

OPCIONES_PAGO = [
    "Menos de $600 MXN",
    "Entre $600 y $1,000 MXN",
    "Entre $1,000 y $2,000 MXN",
    "Más de $2,000 MXN"
]

LUGARES_EVENTO = ["Edén", "La Cañada", "Las Cañas", "Otro"]

MESES_PREFERIDOS = [
    "Sin preferencia",
    "Enero 2027",
    "Febrero 2027",
    "Marzo 2027",
    "Abril 2027",
]

# --- Escala Likert ---
LIKERT_OPTIONS = [
    "Nada importante",
    "Poco importante",
    "Neutral",
    "Importante",
    "Muy importante"
]
LIKERT_TO_NUM = {label: i + 1 for i, label in enumerate(LIKERT_OPTIONS)}
NUM_TO_LIKERT = {i + 1: label for i, label in enumerate(LIKERT_OPTIONS)}

# --- Aspectos del evento (col_csv → etiqueta) ---
ASPECTOS_EVENTO = {
    "likert_ceremonia": "Ceremonia / Protocolo formal",
    "likert_cena": "Cena / Banquete",
    "likert_bebidas": "Barra de bebidas",
    "likert_foto": "Fotografía profesional",
    "likert_video": "Video profesional",
    "likert_photobooth": "Photo booth",
    "likert_decoracion": "Decoración del lugar",
    "likert_iluminacion": "Iluminación ambiental",
    "likert_recuerdos": "Recuerdos / Souvenirs",
    "likert_transporte": "Transporte",
    "likert_afterparty": "After party",
    "likert_tematica": "Temática / Dress code",
}

# --- Géneros musicales (col_csv → etiqueta) ---
GENEROS_MUSICALES = {
    "musica_banda": "Banda / Regional mexicano",
    "musica_cumbia": "Cumbia",
    "musica_reggaeton": "Reggaetón",
    "musica_pop_es": "Pop en español",
    "musica_pop_en": "Pop en inglés",
    "musica_rock": "Rock",
    "musica_electronica": "Electrónica / EDM",
    "musica_salsa": "Salsa / Bachata",
    "musica_hiphop": "Hip-hop / Rap",
    "musica_corridos": "Corridos tumbados",
    "musica_envivo": "Música en vivo (grupo/banda)",
    "musica_dj": "DJ",
}

# --- Servicios por mesa (col_csv → etiqueta) ---
SERVICIOS_MESA = {
    "mesa_centro": "Centro de mesa decorativo",
    "mesa_manteleria": "Mantelería especial",
    "mesa_botellas": "Botellas en mesa (vino/espumoso)",
    "mesa_botana": "Botana o snacks en mesa",
    "mesa_senalizacion": "Señalización con nombres",
}

# --- General ---
ADMIN_PASSWORD = "fime2026"
DATA_DIR = "data"
DATA_FILE = "data/registros.csv"
COOKIE_NAME = "fime_registro_completado"
