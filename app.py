import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mat_co

# Configuración de la página
st.set_page_config(page_title="Simulador de Dispersión", layout="wide")

# --- MODELO 1: TU MODELO GAUSSIANO COMPLETO ---
def modelo_gaussiano_actual():
    st.title("🌬️ Simulador de Dispersión de Contaminantes de fuente continua")
    st.markdown("Ajusta los parámetros en la barra lateral para ver la pluma contaminante.")
    
    # --- BARRA LATERAL (INPUTS) ---
    st.sidebar.header("Configuración de Parámetros")
    
    clase_estabilidad = st.sidebar.selectbox(
        'Clase de estabilidad de Pasquill (CL)',
        ['A', 'B', 'C', 'D', 'E', 'F'],
        index=5
    )
    
    q = st.sidebar.number_input('Tasa de emisión (q) [g/s]', value=166.7)
    u = st.sidebar.slider('Velocidad del viento (u) [m/s]', 0.1, 20.0, 1.0)
    h = st.sidebar.slider('Altura de la fuente (h) [m]', 0.0, 100.0, 5.0)
    zr = st.sidebar.slider('Altura del receptor (zr) [m]', 0.0, 50.0, 0.1)
    
    with st.sidebar.expander("Límites del Dominio"):
        lim = st.number_input('Límite horizontal [m]', value=14000.0)
        lim_y = st
