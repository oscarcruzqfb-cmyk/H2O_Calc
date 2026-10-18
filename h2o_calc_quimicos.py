import math
from pathlib import Path
import streamlit as st

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
st.set_page_config(
    page_title="Calculadora Sistemas H2O Integrales",
    page_icon="💧",
    layout="centered",
)

NAVY = "#0B2545"
TEAL = "#00A8B5"

st.markdown(
    f"""
    <style>
        .stApp {{
            background: linear-gradient(180deg, #ffffff 0%, #f7fcfd 100%);
        }}
        h1, h2, h3 {{
            color: {NAVY};
        }}
        .h2o-subtitle {{
            color: {TEAL};
            font-weight: 600;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# LOGO Y ENCABEZADO
# ============================================================
logo_candidates = [
    Path("logo.png"),
    Path("Sistemas H2O Integrales Logo.png"),
]

for logo in logo_candidates:
    if logo.exists():
        st.image(str(logo), width=220)
        break

st.title("Calculadora Sistemas H2O Integrales")
st.markdown(
    '<div class="h2o-subtitle">Plataforma de Cálculo Técnico para Tratamiento de Agua</div>',
    unsafe_allow_html=True,
)
st.divider()

# ============================================================
# 1. CÁLCULO DE VOLUMEN
# ============================================================
st.header("1. Determinación de Volumen")

metodo_volumen = st.radio(
    "Seleccione el método de captura:",
    [
        "Calcular dimensiones de la piscina/spa",
        "Ya conozco mi volumen (Ingreso manual)",
    ],
)

volumen_final = 0.0

if metodo_volumen == "Ya conozco mi volumen (Ingreso manual)":
    volumen_final = st.number_input(
        "Ingrese el volumen exacto en m³:",
        min_value=0.1,
        value=50.0,
        step=1.0,
    )

else:
    forma = st.selectbox(
        "Seleccione la forma de la instalación:",
        [
            "Rectangular (Tradicional)",
            "Profundidad Variable",
            "Spa Circular (Con Asiento)",
        ],
    )

    if forma == "Rectangular (Tradicional)":
        col1, col2, col3 = st.columns(3)

        largo = col1.number_input("Largo (m)", min_value=0.1, value=7.0, step=0.5)
        ancho = col2.number_input("Ancho (m)", min_value=0.1, value=5.0, step=0.5)
        profundidad = col3.number_input("Profundidad (m)", min_value=0.1, value=1.4, step=0.1)

        volumen_final = largo * ancho * profundidad

    elif forma == "Profundidad Variable":
        st.caption("Se calculará usando la profundidad promedio.")

        col1, col2 = st.columns(2)

        largo = col1.number_input("Largo (m)", min_value=0.1, value=7.0, step=0.5)
        ancho = col2.number_input("Ancho (m)", min_value=0.1, value=5.0, step=0.5)
        prof1 = col1.number_input(
            "Profundidad 1 - Menos profunda (m)",
            min_value=0.1,
            value=1.2,
            step=0.1,
        )
        prof2 = col2.number_input(
            "Profundidad 2 - Más profunda (m)",
            min_value=0.1,
            value=1.75,
            step=0.1,
        )

        prof_promedio = (prof1 + prof2) / 2
        st.info(f"Profundidad promedio: **{prof_promedio:.2f} m**")

        volumen_final = largo * ancho * prof_promedio

    elif forma == "Spa Circular (Con Asiento)":
        st.caption("Cálculo separado por sección de asiento y piso.")

        col1, col2 = st.columns(2)

        d_asiento = col1.number_input(
            "Diámetro 1 - Asiento (m)",
            min_value=0.1,
            value=2.5,
            step=0.1,
        )
        p_asiento = col1.number_input(
            "Profundidad 1 - Asiento (m)",
            min_value=0.1,
            value=0.4,
            step=0.1,
        )

        d_suelo = col2.number_input(
            "Diámetro 2 - Piso (m)",
            min_value=0.1,
            value=2.0,
            step=0.1,
        )
        p_suelo = col2.number_input(
            "Profundidad 2 - Piso (m)",
            min_value=0.1,
            value=0.9,
            step=0.1,
        )

        vol_asiento = math.pi * (d_asiento**2 / 4) * p_asiento
        vol_suelo = math.pi * (d_suelo**2 / 4) * p_suelo

        volumen_final = vol_asiento + vol_suelo

st.success(f"🌊 **Volumen de trabajo: {volumen_final:.2f} m³**")
st.divider()

# ============================================================
# 2. DOSIS DE DESINFECTANTE
# ============================================================
st.header("2. Dosis de Desinfectante")
st.write(f"Volumen utilizado para el cálculo: **{volumen_final:.2f} m³**")

col_d1, col_d2 = st.columns(2)

with col_d1:
    ppm_deseadas = st.number_input(
        "PPM a elevar",
        min_value=0.1,
        value=1.0,
        step=0.1,
    )

with col_d2:
    producto = st.selectbox(
        "Seleccione el desinfectante:",
        [
            "TRICLORO (90%)",
            "DICLORO (60%)",
            "HIPOCLORITO DE SODIO (10%)",
            "HIPOCLORITO DE CALCIO (65%)",
        ],
    )

concentraciones = {
    "TRICLORO (90%)": 0.90,
    "DICLORO (60%)": 0.60,
    "HIPOCLORITO DE SODIO (10%)": 0.10,
    "HIPOCLORITO DE CALCIO (65%)": 0.65,
}

densidad_hipoclorito = 1.13  # kg/L = g/mL

if st.button("Calcular Desinfectante", type="primary"):
    concentracion = concentraciones[producto]

    # 1 ppm en 1 m³ = 1 g de ingrediente activo.
    gramos_producto = (ppm_deseadas * volumen_final) / concentracion

    if producto == "HIPOCLORITO DE SODIO (10%)":
        mililitros = gramos_producto / densidad_hipoclorito

        st.success(
            f"💧 Dosis recomendada: **{mililitros:.0f} mL "
            f"({mililitros/1000:.2f} L)** de {producto}"
        )
    else:
        st.success(
            f"⚖️ Dosis recomendada: **{gramos_producto:.0f} g "
            f"({gramos_producto/1000:.2f} kg)** de {producto}"
        )

    st.caption(
        "Cálculo teórico. Verifique siempre la concentración indicada "
        "en la ficha técnica del producto."
    )

st.divider()

# ============================================================
# 3. AJUSTE DE pH
# ============================================================
st.header("3. Ajuste de pH")

ph_actual = st.number_input(
    "Ingrese el pH actual medido:",
    min_value=0.0,
    max_value=14.0,
    value=7.2,
    step=0.1,
)

# Tablas de referencia de la versión original.
# Dosis expresadas por cada 10 m³.
tabla_carbonato = {
    6.2: 1400,
    6.6: 1100,
    6.8: 700,
    7.0: 400,
}

tabla_bisulfato = {
    7.6: 120,
    7.8: 220,
    8.0: 340,
    8.2: 500,
    8.4: 580,
}

if st.button("Analizar y Calcular pH", type="secondary"):

    if 7.1 <= ph_actual <= 7.5:
        st.success(
            "✅ **pH dentro del rango de trabajo. "
            "No se requiere ajuste químico según esta tabla.**"
        )

    elif ph_actual < 6.2:
        st.error(
            "🚨 **pH críticamente bajo. "
            "Requiere evaluación técnica antes de dosificar.**"
        )

    elif ph_actual > 8.4:
        st.error(
            "🚨 **pH críticamente alto. "
            "Requiere evaluación técnica antes de dosificar.**"
        )

    elif 6.2 <= ph_actual <= 7.0:
        st.warning("⚠️ El pH está bajo. Se requiere Carbonato de Sodio.")

        ph_claves = sorted(tabla_carbonato.keys(), reverse=True)
        dosis_base = tabla_carbonato[6.2]
        ph_usado = 6.2

        for clave in ph_claves:
            if ph_actual >= clave:
                dosis_base = tabla_carbonato[clave]
                ph_usado = clave
                break

        gramos_totales = (volumen_final / 10) * dosis_base

        st.info(f"Se utilizó el valor de referencia de pH **{ph_usado:.1f}**.")
        st.success(
            f"⚖️ Dosis recomendada: **{gramos_totales:.0f} g "
            f"({gramos_totales/1000:.2f} kg)** de Carbonato de Sodio."
        )

    elif 7.6 <= ph_actual <= 8.4:
        st.warning("⚠️ El pH está alto. Se requiere Bisulfato de Sodio.")

        ph_claves = sorted(tabla_bisulfato.keys())
        dosis_base = tabla_bisulfato[8.4]
        ph_usado = 8.4

        for clave in ph_claves:
            if ph_actual <= clave:
                dosis_base = tabla_bisulfato[clave]
                ph_usado = clave
                break

        gramos_totales = (volumen_final / 10) * dosis_base

        st.info(f"Se utilizó el valor de referencia de pH **{ph_usado:.1f}**.")
        st.success(
            f"⚖️ Dosis recomendada: **{gramos_totales:.0f} g "
            f"({gramos_totales/1000:.2f} kg)** de Bisulfato de Sodio."
        )

    st.caption(
        "Las dosis son valores de referencia. Dosifique por etapas, mantenga "
        "la recirculación y vuelva a medir antes de realizar una segunda corrección."
    )

st.divider()
st.caption("© Sistemas H2O Integrales · Calculadora de dosificación química")
