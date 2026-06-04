import streamlit as st
import math

# =====================================================================
# 1. CONFIGURACIÓN VISUAL Y DE MARCA
# =====================================================================
st.set_page_config(page_title="Calculadora Sistemas H2O Integrales", page_icon="💧", layout="centered")

try:
    st.image("Sistemas H2O Integrales Logo.png", width=220)
except:
    st.caption("Coloca el logo en la misma carpeta para visualizar la identidad de la marca.")

st.title("Calculadora Sistemas H2O Integrales")
st.markdown("*Plataforma de Cálculo Técnico para Tratamiento de Agua*")
st.write("---")

# =====================================================================
# 2. MÓDULO 1: CÁLCULO DE VOLUMEN
# =====================================================================
st.header("1. Determinación de Volumen (m³)")

metodo_volumen = st.radio(
    "Seleccione el método de captura:",
    ["Calcular dimensiones de la piscina/spa", "Ya conozco mi volumen (Ingreso manual)"]
)

volumen_final = 0.0

if metodo_volumen == "Ya conozco mi volumen (Ingreso manual)":
    volumen_final = st.number_input("Ingrese el volumen exacto en m³:", min_value=1.0, value=50.0, step=1.0)
else:
    forma = st.selectbox("Seleccione la forma de la instalación:", 
                         ["Rectangular (Tradicional)", "Profundidad Variable", "Spa Circular (Con Asiento)"])
    
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
        prof1 = col1.number_input("Profundidad 1 (Menos profunda en m)", min_value=0.1, value=1.2, step=0.1)
        prof2 = col2.number_input("Profundidad 2 (Más profunda en m)", min_value=0.1, value=1.75, step=0.1)
        
        prof_promedio = (prof1 + prof2) / 2
        st.info(f"Profundidad Promedio calculada: **{prof_promedio:.3f} m**")
        volumen_final = largo * ancho * prof_promedio
        
    elif forma == "Spa Circular (Con Asiento)":
        st.caption("Cálculo separado por sección de suelo y asiento.")
        col1, col2 = st.columns(2)
        d_asiento = col1.number_input("Diámetro 1 - Asiento (m)", min_value=0.1, value=2.5, step=0.1)
        p_asiento = col1.number_input("Profundidad 1 - Asiento (m)", min_value=0.1, value=0.4, step=0.1)
        d_suelo = col2.number_input("Diámetro 2 - Piso (m)", min_value=0.1, value=2.0, step=0.1)
        p_suelo = col2.number_input("Profundidad 2 - Piso (m)", min_value=0.1, value=0.9, step=0.1)
        
        vol_asiento = ((d_asiento**2) / 4) * math.pi * p_asiento
        vol_suelo = ((d_suelo**2) / 4) * math.pi * p_suelo
        volumen_final = vol_asiento + vol_suelo

st.success(f"🌊 **Volumen de Trabajo:** {volumen_final:.2f} m³")
st.write("---")

# =====================================================================
# 3. MÓDULO 2: DESINFECTANTE
# =====================================================================
st.header("2. Dosis de Desinfectante")
st.write(f"Utilizando el volumen calculado de: **{volumen_final:.2f} m³**")

col_d1, col_d2 = st.columns(2)
with col_d1:
    ppm_deseadas = st.number_input("PPM a elevar", min_value=0.1, value=1.0, step=0.1)
with col_d2:
    producto = st.selectbox("Selecciona el Desinfectante", 
                            ["TRICLORO (90%)", "DICLORO (60%)", "HIPOCLORITO DE SODIO (10%)", "HIPOCLORITO DE CALCIO (65%)"])

concentraciones = {
    "TRICLORO (90%)": 0.9,
    "DICLORO (60%)": 0.6,
    "HIPOCLORITO DE SODIO (10%)": 0.1,  
    "HIPOCLORITO DE CALCIO (65%)": 0.65
}
densidad_hipoclorito = 1.13  # g/ml

if st.button("Calcular Desinfectante", type="primary"):
    concentracion = concentraciones[producto]
    gramos = (ppm_deseadas * volumen_final) / concentracion
    
    if producto == "HIPOCLORITO DE SODIO (10%)":
        mililitros = gramos / densidad_hipoclorito
        st.success(f"💧 Dosis recomendada: **{mililitros:.2f} mililitros (ml)** de {producto}")
    else:
        st.success(f"⚖️ Dosis recomendada: **{gramos:.2f} gramos** de {producto}")

st.write("---")

# =====================================================================
# 4. MÓDULO 3: AJUSTE DE pH
# =====================================================================
st.header("3. Ajuste de pH")
ph_actual = st.number_input("Ingrese el pH actual medido:", min_value=0.0, max_value=14.0, value=7.2, step=0.1)

# Tablas maestras alimentadas directamente desde tu Excel
tabla_carbonato = {
    6.2: 1400,
    6.6: 1100,
    6.8: 700,
    7.0: 400
}

tabla_bisulfato = {
    7.6: 120,
    7.8: 220,
    8.0: 340,
    8.2: 500,
    8.4: 580
}

if st.button("Analizar y Calcular pH", type="secondary"):
    if 7.1 <= ph_actual <= 7.5:
        st.success("✅ **pH en rango ideal. No se requiere ajuste químico.**")
        
    elif ph_actual < 6.2:
        st.error("🚨 **pH críticamente bajo, requiere evaluación técnica presencial.**")
        
    elif ph_actual > 8.4:
        st.error("🚨 **pH críticamente alto, requiere evaluación técnica presencial.**")
        
    elif 6.2 <= ph_actual <= 7.0:
        st.warning("⚠️ El pH está bajo. Se requiere Carbonato de Sodio.")
        # Lógica de aproximación al valor INFERIOR más cercano
        ph_claves = sorted(tabla_carbonato.keys(), reverse=True)
        dosis_base = tabla_carbonato[6.2]
        ph_usado = 6.2
        for clave in ph_claves:
            if ph_actual >= clave:
                dosis_base = tabla_carbonato[clave]
                ph_usado = clave
                break
        
        gramos_totales = (volumen_final / 10) * dosis_base
        st.info(f"*(Se utilizó el parámetro de pH {ph_usado} de la tabla de referencia para aproximar por el valor inferior más cercano)*")
        st.success(f"⚖️ Dosis recomendada: **{gramos_totales:.2f} gramos** de Carbonato de Sodio.")
        
    elif 7.6 <= ph_actual <= 8.4:
        st.warning("⚠️ El pH está alto. Se requiere Bisulfato de Sodio.")
        # Lógica de aproximación al valor SUPERIOR más cercano
        ph_claves = sorted(tabla_bisulfato.keys())
        dosis_base = tabla_bisulfato[8.4]
        ph_usado = 8.4
        for clave in ph_claves:
            if ph_actual <= clave:
                dosis_base = tabla_bisulfato[clave]
                ph_usado = clave
                break
        
        gramos_totales = (volumen_final / 10) * dosis_base
        st.info(f"*(Se utilizó el parámetro de pH {ph_usado} de la tabla de referencia para aproximar por el valor superior más cercano)*")
        st.success(f"⚖️ Dosis recomendada: **{gramos_totales:.2f} gramos** de Bisulfato de Sodio.")