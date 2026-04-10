import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mat_co

# Configuración global
st.set_page_config(page_title="Simulador de Dispersión", layout="wide")

# Selector de Modelo en la barra lateral con los nuevos nombres
st.sidebar.title("Navegación")
modelo_seleccionado = st.sidebar.radio(
    "Selecciona el modelo:", 
    ["Modelo 1: Emisión continua", "Modelo 2: Emisión tipo puff"]
)

# ---------------------------------------------------------
# MODELO 1: EMISIÓN CONTINUA (PLUMA)
# ---------------------------------------------------------
def ejecutar_modelo_1():
    # Título de pantalla coincidente
    st.title("🌬️ Modelo 1: Emisión continua")
    st.sidebar.header("Parámetros Modelo 1")

    clase_estabilidad = st.sidebar.selectbox(
        'Clase de estabilidad de Pasquill (CL)',
        ['A', 'B', 'C', 'D', 'E', 'F'], index=5, key="cl1"
    )

    q = st.sidebar.number_input('Tasa de emisión (q) [g/s]', value=166.7, key="q1")
    u = st.sidebar.slider('Velocidad del viento (u) [m/s]', 0.1, 20.0, 1.0, key="u1")
    h = st.sidebar.slider('Altura de la fuente (h) [m]', 0.0, 100.0, 5.0, key="h1")
    zr = st.sidebar.slider('Altura del receptor (zr) [m]', 0.0, 50.0, 0.1, key="zr1")

    with st.sidebar.expander("Límites del Dominio"):
        lim = st.number_input('Límite horizontal [m]', value=14000.0)
        lim_y = st.number_input('Límite transversal [m]', value=2800.0)

    # Lógica de cálculo
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
    X, Y = np.meshgrid(x, y)

    sig_y = ay * X ** by
    sig_z = az * X ** bz

    Conc = q / (2 * np.pi * u * (ay * x ** by) * (az * x ** bz)) * np.exp(-(zr - h) ** 2 / (2 * (az * x ** bz) ** 2))
    Conc_con = q / (2 * np.pi * u * sig_y * sig_z) * np.exp(-Y ** 2 / (2 * sig_y ** 2)) * np.exp(-(zr - h) ** 2 / (2 * sig_z ** 2))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Concentración Lineal")
        fig1, ax1 = plt.subplots()
        ax1.plot(x, Conc, color='red')
        ax1.set_xlabel('Distancia [m]')
        ax1.set_ylabel('Concentración [g/m³]')
        st.pyplot(fig1)
        st.metric("Concentración Máxima", f"{Conc.max():.2e} g/m³")

    with col2:
        st.subheader("Vista Superior (XY)")
        cmap = mat_co.ListedColormap(['white', 'LightBlue', 'Deepskyblue', 'SpringGreen', 'yellow', 'orange', 'red'])
        c_max = Conc.max() if Conc.max() > 0 else 1e-10
        levels = np.logspace(np.log10(c_max*1e-5), np.log10(c_max), 7)
        fig2, ax2 = plt.subplots()
        norm = mat_co.BoundaryNorm(levels, cmap.N, clip=True)
        CS = ax2.contourf(X, Y, Conc_con, levels=levels, cmap=cmap, norm=norm)
        plt.colorbar(CS, label='g/m³')
        st.pyplot(fig2)

# ---------------------------------------------------------
# MODELO 2: EMISIÓN TIPO PUFF
# ---------------------------------------------------------
def ejecutar_modelo_2():
    # Título de pantalla coincidente
    st.title("⏱️ Modelo 2: Emisión tipo puff")
    st.sidebar.header("Parámetros Modelo 2")

    CL2 = st.sidebar.selectbox('Estabilidad (CL)', ['A', 'B', 'C', 'D', 'E', 'F'], index=5, key="cl2")
    q2 = st.sidebar.number_input('Masa liberada (q) [g]', value=100.0, key="q2")
    u2 = st.sidebar.slider('Velocidad viento (u) [m/s]', 0.1, 20.0, 2.0, key="u2")
    h2 = st.sidebar.slider('Altura fuente (h) [m]', 0, 100, 20, key="h2")

    k_map = {'A': 50, 'B': 25, 'C': 12.5, 'D': 6.25, 'E': 3.125, 'F': 1.5}
    K = k_map[CL2]
    K_x = K_y = K_z = K

    lim2 = 2000.0
    t = np.linspace(0.1, lim2/u2, 200)

    def calc_c(xr_val, tiempo):
        Fd = q2 / (8 * (np.pi * tiempo)**(1.5) * (K_x * K_y * K_z)**(0.5))
        return Fd * np.exp(-(xr_val - u2*tiempo)**2 / (4*K_x*tiempo))

    st.subheader(f"Concentración en el tiempo (CE {CL2})")
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(t, calc_c(250, t), label='250 m')
    ax3.plot(t, calc_c(500, t), label='500 m')
    ax3.plot(t, calc_c(1000, t), label='1000 m')
    ax3.set_xlabel("Tiempo desde la liberación [s]")
    ax3.set_ylabel("Concentración [g/m³]")
    ax3.legend()
    st.pyplot(fig3)

# ---------------------------------------------------------
# LÓGICA DE CONTROL
# ---------------------------------------------------------
if modelo_seleccionado == "Modelo 1: Emisión continua":
    ejecutar_modelo_1()
else:
    ejecutar_modelo_2()
