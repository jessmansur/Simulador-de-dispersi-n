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
    st.sidebar.header("Parámetros del Segundo Modelo")
        
        # 1. Estas variables ahora se controlan desde la web
        CL = st.sidebar.selectbox('Estabilidad (CL)', ['A', 'B', 'C', 'D', 'E', 'F'], index=5)
        u = st.sidebar.slider('Velocidad viento (u) [m/s]', 0.1, 20.0, 2.0)
        q = st.sidebar.number_input('Emisión (q) [g/s]', value=100.0)
        h = st.sidebar.slider('Altura de la fuente (h) [m]', 0, 100, 20)
        
        # Parámetros fijos del receptor
        zr = 0 
        yr = 0 
        lim = 2000. 
        lim_1 = 600. 
        
        # 2. Lógica de Estabilidad
        if CL == 'A':
            f_e_y, K_x, K_y, K_z = 5, 50, 50, 50
        elif CL == 'B':
            f_e_y, K_x, K_y, K_z = 2, 25, 25, 25
        elif CL == 'C':
            f_e_y, K_x, K_y, K_z = 5, 12.5, 12.5, 12.5
        elif CL == 'D':
            f_e_y, K_x, K_y, K_z = 10, 6.25, 6.25, 6.25
        elif CL == 'E':
            f_e_y, K_x, K_y, K_z = 10, 3.125, 3.125, 3.125
        elif CL == 'F':
            f_e_y, K_x, K_y, K_z = 5, 1.5, 1.5, 1.5
    
        # 3. Cálculos de mallas y tiempo
        x = np.arange(0.1, lim, lim/100)
        y = np.arange(-lim/f_e_y, lim/f_e_y, lim/f_e_y/100)
        z = np.arange(0.1, lim_1, lim_1/100)
        t = np.arange(0.1, lim/u, lim/u/100)
        
        X, Y = np.meshgrid(x, y)
        
        # 4. Cálculo de concentraciones en diferentes distancias
        def calcular_conc(dist_x, tiempo, q_em, u_viento, kx, ky, kz):
            Fd = q_em / (8 * (np.pi * tiempo)**(3/2) * (kx * ky * kz)**(1/2))
            cx = np.exp(-(dist_x - u_viento * tiempo)**2 / (4 * kx * tiempo))
            cy = np.exp(-(0)**2 / (4 * ky * tiempo)) # yr = 0
            cz = np.exp(-(0)**2 / (4 * kz * tiempo)) # zr = 0
            return Fd * cx * cy * cz
    
        Conc_0 = calcular_conc(250, t, q, u, K_x, K_y, K_z)
        Conc = calcular_conc(500, t, q, u, K_x, K_y, K_z)
        Conc_1 = calcular_conc(1000, t, q, u, K_x, K_y, K_z)
        Conc_2 = calcular_conc(1500, t, q, u, K_x, K_y, K_z)
    
        # --- GRÁFICO 1: TIEMPO ---
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.plot(t, Conc_0, label='250m')
        ax1.plot(t, Conc, label='500m')
        ax1.plot(t, Conc_1, label='1000m')
        ax1.plot(t, Conc_2, label='1500m')
        ax1.set_title(f'Concentración con Estabilidad {CL}')
        ax1.set_xlabel('Tiempo [s]')
        ax1.set_ylabel('Concentración [g/m³]')
        ax1.legend()
        st.pyplot(fig1)
    
        # --- GRÁFICO 2: MAPAS DE CALOR (6 subplots) ---
        st.write("### Evolución Espacial de la Pluma")
        tiempos_mapa = [50, 100, 125, 150, 250, 500]
        fig2, axes = plt.subplots(3, 2, figsize=(12, 12))
        axes = axes.flatten()
    
        for i, T in enumerate(tiempos_mapa):
            C_map = (q / (8 * (np.pi * T)**(3/2) * (K_x * K_y * K_z)**(1/2)) *
                     np.exp(-(X - u * T)**2 / (4 * K_x * T)) *
                     np.exp(-(Y)**2 / (4 * K_y * T)) *
                     np.exp(-(0)**2 / (4 * K_z * T)))
            
            im = axes[i].contourf(X, Y, C_map, cmap='jet')
            axes[i].set_title(f'Tiempo: {T}s')
            plt.colorbar(im, ax=axes[i])
    
        plt.tight_layout()
        st.pyplot(fig2)
