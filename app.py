import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mat_co

# 1. CONFIGURACIÓN DE PÁGINA (Debe ir arriba de todo)
st.set_page_config(page_title="Simulador de Dispersión", layout="wide")

# --- FUNCIONES DE LOS MODELOS ---

def modelo_gaussiano_actual():
    st.title("🌬️ Simulador de Dispersión de Contaminantes")
    st.markdown("Ajusta los parámetros en la barra lateral.")
    
    # --- BARRA LATERAL (INPUTS) ---
    st.sidebar.header("Configuración de Parámetros")
    clase_estabilidad = st.sidebar.selectbox('Clase de estabilidad de Pasquill (CL)',['A', 'B', 'C', 'D', 'E', 'F'], index=5)
    q = st.sidebar.number_input('Tasa de emisión (q) [g/s]', value=166.7)
    u = st.sidebar.slider('Velocidad del viento (u) [m/s]', 0.1, 20.0, 1.0)
    h = st.sidebar.slider('Altura de la fuente (h) [m]', 0.0, 100.0, 5.0)
    zr = st.sidebar.slider('Altura del receptor (zr) [m]', 0.0, 50.0, 0.1)
    
    with st.sidebar.expander("Límites del Dominio"):
        lim = st.number_input('Límite horizontal [m]', value=14000.0)
        lim_y = st.number_input('Límite transversal [m]', value=2800.0)
        lim_z = st.number_input('Límite vertical [m]', value=5000.0)

    # --- LÓGICA DE CÁLCULO ---
    params = {'A': (0.469, 0.903, 0.017, 1.380), 'B': (0.306, 0.885, 0.072, 1.021), 'C': (0.230, 0.855, 0.076, 0.879), 'D': (0.219, 0.764, 0.140, 0.727), 'E': (0.237, 0.691, 0.217, 0.610), 'F': (0.273, 0.594, 0.262, 0.500)}
    ay, by, az, bz = params[clase_estabilidad]
    
    x = np.linspace(0.1, lim, 200)
    y = np.linspace(-lim_y/2, lim_y/2, 150)
    X, Y = np.meshgrid(x, y)
    
    sig_y = ay * X ** by
    sig_z = az * X ** bz
    
    # Concentraciones
    Conc = q / (2 * np.pi * u * (ay * x ** by) * (az * x ** bz)) * np.exp(-(zr - h) ** 2 / (2 * (az * x ** bz) ** 2))
    Conc_con = q / (2 * np.pi * u * sig_y * sig_z) * np.exp(-Y ** 2 / (2 * sig_y ** 2)) * np.exp(-(zr - h) ** 2 / (2 * sig_z ** 2))
    
    # --- VISUALIZACIÓN ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Gráfico de Concentración Lineal")
        fig1, ax1 = plt.subplots()
        ax1.plot(x, Conc, color='red')
        ax1.set_xlabel('Distancia [m]')
        ax1.set_ylabel('Concentración [g/m³]')
        st.pyplot(fig1)
        st.metric("Concentración Máxima", f"{Conc.max():.2e} g/m³")
    
    with col2:
        st.subheader("Plano Horizontal (Vista Superior)")
        fig2, ax2 = plt.subplots()
        cmap = mat_co.ListedColormap(['white', 'LightBlue', 'Deepskyblue', 'SpringGreen', 'yellow', 'orange', 'red'])
        CS = ax2.contourf(X, Y, Conc_con, cmap=cmap)
        plt.colorbar(CS)
        ax2.set_xlabel('Distancia viento [m]')
        ax2.set_ylabel('Distancia perpendicular [m]')
        st.pyplot(fig2)

def nuevo_modelo():
    st.title("🧪 Segundo Modelo de Dispersión")
    st.info("Esta sección está lista para recibir tu nuevo código.")
    st.write("Usa el menú de la izquierda para volver al modelo original.")

# --- LÓGICA DE NAVEGACIÓN (Esto va pegado al borde izquierdo) ---

st.sidebar.markdown("---")
opcion = st.sidebar.selectbox(
    "Selecciona el modelo:",
    ("Modelo Gaussiano Actual", "Nuevo Modelo de Dispersión")
)

if opcion == "Modelo Gaussiano Actual":
    modelo_gaussiano_actual()
else:
    nuevo_modelo()
