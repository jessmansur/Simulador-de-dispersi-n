import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mat_co

# Configuración de la página
st.set_page_config(page_title="Simulador de Dispersión Gaussiana", layout="wide")

st.title("🌬️ Simulador de Dispersión de Contaminantes")
st.markdown("Ajusta los parámetros en la barra lateral para ver cómo se desplaza la pluma contaminante.")

# -------------------------------
# BARRA LATERAL (INPUTS)
# -------------------------------
st.sidebar.header("Configuración de Parámetros")

clase_estabilidad = st.sidebar.selectbox(
    'Clase de estabilidad de Pasquill (CL)',
    ['A', 'B', 'C', 'D', 'E', 'F'],
    index=5  # Por defecto 'F' como en tu script
)

q = st.sidebar.number_input('Tasa de emisión (q) [g/s]', value=166.7)
u = st.sidebar.slider('Velocidad del viento (u) [m/s]', 0.1, 20.0, 1.0)
h = st.sidebar.slider('Altura de la fuente (h) [m]', 0.0, 100.0, 5.0)
zr = st.sidebar.slider('Altura del receptor (zr) [m]', 0.0, 50.0, 0.1)

with st.sidebar.expander("Límites del Dominio"):
    lim = st.number_input('Límite horizontal [m]', value=14000.0)
    lim_y = st.number_input('Límite transversal [m]', value=2800.0)
    lim_z = st.number_input('Límite vertical [m]', value=5000.0)

# -------------------------------
# LÓGICA DE CÁLCULO
# -------------------------------
params = {
    'A': (0.469, 0.903, 0.017, 1.380),
    'B': (0.306, 0.885, 0.072, 1.021),
    'C': (0.230, 0.855, 0.076, 0.879),
    'D': (0.219, 0.764, 0.140, 0.727),
    'E': (0.237, 0.691, 0.217, 0.610),
    'F': (0.273, 0.594, 0.262, 0.500),
}

ay, by, az, bz = params[clase_estabilidad]

x = np.linspace(0.1, lim, 200)
y = np.linspace(-lim_y/2, lim_y/2, 150)
z = np.linspace(0.1, lim_z, 150)

X, Y = np.meshgrid(x, y)
X1, Z = np.meshgrid(x, z)

sig_y = ay * X ** by
sig_z = az * X ** bz

# Concentraciones
Conc = q / (2 * np.pi * u * (ay * x ** by) * (az * x ** bz)) * np.exp(-(zr - h) ** 2 / (2 * (az * x ** bz) ** 2))

Conc_con = q / (2 * np.pi * u * sig_y * sig_z) * \
           np.exp(-Y ** 2 / (2 * sig_y ** 2)) * \
           np.exp(-(zr - h) ** 2 / (2 * sig_z ** 2))

# -------------------------------
# VISUALIZACIÓN EN LA WEB
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Gráfico de Concentración Lineal")
    fig1, ax1 = plt.subplots()
    ax1.plot(x, Conc, color='red')
    ax1.set_xlabel('Distancia [m]')
    ax1.set_ylabel('Concentración [g/m³]')
    ax1.grid(True, alpha=0.3)
    st.pyplot(fig1)
    st.metric("Concentración Máxima", f"{Conc.max():.2e} g/m³")

with col2:
    st.subheader("Plano Horizontal (Vista Superior)")
    cmap = mat_co.ListedColormap(['white', 'LightBlue', 'Deepskyblue', 'SpringGreen', 'yellow', 'orange', 'red'])
    
    # Manejo dinámico de niveles para evitar errores si Conc.max es muy bajo
    c_max = Conc.max() if Conc.max() > 0 else 1e-10
    ccmi = 10 ** int(np.log10(1E-5 * c_max))
    ccma = 10 ** int(np.log10(c_max))
    levels = sorted(list(set([ccmi * 10, ccmi * 100, ccmi * 1000, ccmi * 10000, ccma, ccma * 10])))
    
    fig2, ax2 = plt.subplots()
    norm = mat_co.BoundaryNorm(levels, cmap.N, clip=True)
    CS = ax2.contourf(X, Y, Conc_con, levels, cmap=cmap, norm=norm)
    plt.colorbar(CS, label='g/m³')
    ax2.set_xlabel('Distancia viento [m]')
    ax2.set_ylabel('Distancia perpendicular [m]')
    st.pyplot(fig2)
