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
    CL='F'
q = 100 # g/s
u = 2 # m/s
h = 20 # m

zr=0 #m
xr = 1000 #m
yr = 0 #m

lim=2000. # [m] Límite en el plano horizontal
lim_1 = 600. # [m] Límite de altura


if CL=='A' :
    f_e_y = 5
    K_x = 50
    K_y = 50
    K_z = 50

if CL=='B' :
    f_e_y = 2
    K_x = 25
    K_y = 25
    K_z = 25

if CL=='C' :
    f_e_y = 5
    K_x = 12.5
    K_y = 12.5
    K_z = 12.5

if CL=='D' :
    f_e_y = 10
    K_x = 6.25
    K_y = 6.25
    K_z = 6.25

if CL=='E' :
    f_e_y = 10
    K_x = 3.125
    K_y = 3.125
    K_z = 3.125

if CL=='F' :
    f_e_y = 5
    K_x = 1.5
    K_y = 1.5
    K_z = 1.5



x = np.arange(0.1, lim, lim/100)
y = np.arange(-lim/f_e_y, lim/f_e_y, lim/f_e_y/100)
z = np.arange(0.1, lim_1, lim_1/100)
t = np.arange(0.1, lim/u, lim/u/100)




X, Y = np.meshgrid(x, y)
X1, Z = np.meshgrid(x, z)

xr = 250 #m
Fd = q / (8 * (3.14 * t)**(3/2) * (K_x * K_y * K_z)**(1/2))
Conc_x = np.exp(-(xr-u*t)**2 /(4*K_x*t))
Conc_y = np.exp(-(yr - 0)**2 /(4*K_y*t))
Conc_z = np.exp(-(zr- 0)**2 /(4*K_z*t))

Conc_0 = Fd * Conc_x * Conc_y * Conc_z


xr = 500 #m
Fd = q / (8 * (3.14 * t)**(3/2) * (K_x * K_y * K_z)**(1/2))
Conc_x = np.exp(-(xr-u*t)**2 /(4*K_x*t))
Conc_y = np.exp(-(yr - 0)**2 /(4*K_y*t))
Conc_z = np.exp(-(zr- 0)**2 /(4*K_z*t))

Conc = Fd * Conc_x * Conc_y * Conc_z

xr = 1000
Fd = q / (8 * (3.14 * t)**(3/2) * (K_x * K_y * K_z)**(1/2))
Conc_x = np.exp(-(xr-u*t)**2 /(4*K_x*t))
Conc_y = np.exp(-(yr - 0)**2 /(4*K_y*t))
Conc_z = np.exp(-(zr- 0)**2 /(4*K_z*t))
Conc_1 = Fd * Conc_x * Conc_y * Conc_z

xr = 1500
Fd = q / (8 * (3.14 * t)**(3/2) * (K_x * K_y * K_z)**(1/2))
Conc_x = np.exp(-(xr-u*t)**2 /(4*K_x*t))
Conc_y = np.exp(-(yr - 0)**2 /(4*K_y*t))
Conc_z = np.exp(-(zr- 0)**2 /(4*K_z*t))
Conc_2 = Fd * Conc_x * Conc_y * Conc_z


print()
print()
print('Altura de liberación: ', h ,'m' , '   tasa de liberación: ', q,'g/s')

levels = [1E-12,1E-11,1E-10,1E-9,1E-8,1E-7,1E-6,1E-5,1E-4,1E-3,1E-2,1E-1]
######################################################################################################    
plt.subplots(nrows=1, ncols=1, figsize=(22, 6.5), sharey=True)
#-----------------------------------------------------------------------------------------------------
plt.subplot(111)
titulo ='Concentración para un receptor ubicado a 1000 m con CE ' + CL
plt.title(titulo, fontsize = 'x-large')
plt.ylabel('Concentración [g/m\u00b3]', fontsize = 'x-large')
plt.xlabel('Tiempo desde la liberación [s]',fontsize = 'x-large')
paso = 'Concentración Max  {0:.2e}, {1:.2e}, {2:.2e}, {3:.2e}  g/m\u00b3'.format(Conc_0.max(),Conc.max(),Conc_1.max(),Conc_2.max())
plt.annotate(paso, xy=(lim/u/5, Conc.max()/2),fontsize = 'x-large')
plt.plot(t,Conc_0)
plt.plot(t,Conc)
plt.plot(t, Conc_1)
plt.plot(t,Conc_2)

plt.show()









######################################################################################################    
plt.subplots(nrows=3, ncols=2, figsize=(22, 12), sharey=True)
#-----------------------------------------------------------------------------------------------------
plt.subplot(321)
T = 50 #s

Conc_con =(
        q / (8 * (3.14 * T)**(3/2) * (K_x * K_y * K_z)**(1/2))
        * np.exp(-(X-u*T)**2 /(4*K_x*T))
        * np.exp(-(Y - 0)**2 /(4*K_y*T))
        * np.exp(-(zr- 0)**2 /(4*K_z*T))
        )

cmap = mat_co.ListedColormap(['white','LightBlue','Deepskyblue','SpringGreen', 'yellow','orange', 'red']) #selecciono los colores
ccmi = 10**int(np.log10(1E-5*Conc_con.max()))
ccma = 10**int(np.log10(Conc_con.max()))
if (ccmi == 0.0001):
#    levels = [ccmi,ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma*5,ccma*10]
    levels = [ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma*5,ccma*10]
else:
#    levels = [ccmi,ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma,ccma*10]
    levels = [ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma,ccma*10]


paso = 'Concentración Max  {0:.2e}  g/m\u00b3'.format(Conc_con.max())
plt.annotate(paso, xy=(u*T, lim/f_e_y*.75),fontsize = 'x-large')


norm = mat_co.BoundaryNorm(levels, cmap.N, clip=True)
CS = plt.contourf(X,Y,Conc_con,levels, cmap = cmap,norm=norm)#colors='k')#, linewidths=.5, linestyles=None)
CS1 = plt.contour(X,Y,Conc_con,levels)#colors='k')#, linewidths=.5, linestyles=None)
cbar = plt.colorbar(CS, boundaries=levels)
cbar.ax.set_title('Concentración')
cbar.set_ticklabels([format(levels[0], ".1e"),
                     format(levels[1], ".1e"),
                     format(levels[2], ".1e"),
                     format(levels[3], ".1e"),
                     format(levels[4], ".1e"),
                     format(levels[5], ".1e")])#,
#                     format(levels[6], ".1e")])


plt.subplot(322)

T = 100 #s

Conc_con =(
        q / (8 * (3.14 * T)**(3/2) * (K_x * K_y * K_z)**(1/2))
        * np.exp(-(X-u*T)**2 /(4*K_x*T))
        * np.exp(-(Y - 0)**2 /(4*K_y*T))
        * np.exp(-(zr- 0)**2 /(4*K_z*T))
        )

cmap = mat_co.ListedColormap(['white','LightBlue','Deepskyblue','SpringGreen', 'yellow','orange', 'red']) #selecciono los colores
ccmi = 10**int(np.log10(1E-5*Conc_con.max()))
ccma = 10**int(np.log10(Conc_con.max()))
if (ccmi == 0.0001):
#    levels = [ccmi,ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma*5,ccma*10]
    levels = [ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma*5,ccma*10]
else:
#    levels = [ccmi,ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma,ccma*10]
    levels = [ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma,ccma*10]


CS = plt.contourf(X,Y,Conc_con,levels, cmap = cmap,norm=norm)#colors='k')#, linewidths=.5, linestyles=None)
CS1 = plt.contour(X,Y,Conc_con,levels)#colors='k')#, linewidths=.5, linestyles=None)
cbar = plt.colorbar(CS, boundaries=levels)
cbar.ax.set_title('Concentración')
cbar.set_ticklabels([format(levels[0], ".1e"),
                     format(levels[1], ".1e"),
                     format(levels[2], ".1e"),
                     format(levels[3], ".1e"),
                     format(levels[4], ".1e"),
                     format(levels[5], ".1e")])#,
#                     format(levels[6], ".1e")])

plt.xlabel('Distancia dirección del viento [m]', fontsize = 'x-large')
plt.ylabel('Distancia perp dir del viento [m]',fontsize = 'x-large')
paso = 'Concentración Max  {0:.2e}  g/m\u00b3'.format(Conc_con.max())
plt.annotate(paso, xy=(u*T, lim/f_e_y*.75),fontsize = 'x-large')
#plt.show()

######################################################################################################    
#plt.subplots(nrows=1, ncols=2, figsize=(22, 6.5), sharey=True)
#-----------------------------------------------------------------------------------------------------
plt.subplot(323)
T = 125 #s

Conc_con =(
        q / (8 * (3.14 * T)**(3/2) * (K_x * K_y * K_z)**(1/2))
        * np.exp(-(X-u*T)**2 /(4*K_x*T))
        * np.exp(-(Y - 0)**2 /(4*K_y*T))
        * np.exp(-(zr- 0)**2 /(4*K_z*T))
        )

cmap = mat_co.ListedColormap(['white','LightBlue','Deepskyblue','SpringGreen', 'yellow','orange', 'red']) #selecciono los colores
ccmi = 10**int(np.log10(1E-5*Conc_con.max()))
ccma = 10**int(np.log10(Conc_con.max()))
if (ccmi == 0.0001):
#    levels = [ccmi,ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma*5,ccma*10]
    levels = [ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma*5,ccma*10]
else:
#    levels = [ccmi,ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma,ccma*10]
    levels = [ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma,ccma*10]


CS = plt.contourf(X,Y,Conc_con,levels, cmap = cmap,norm=norm)#colors='k')#, linewidths=.5, linestyles=None)
CS1 = plt.contour(X,Y,Conc_con,levels)#colors='k')#, linewidths=.5, linestyles=None)
cbar = plt.colorbar(CS, boundaries=levels)
cbar.ax.set_title('Concentración')
cbar.set_ticklabels([format(levels[0], ".1e"),
                     format(levels[1], ".1e"),
                     format(levels[2], ".1e"),
                     format(levels[3], ".1e"),
                     format(levels[4], ".1e"),
                     format(levels[5], ".1e")])#,
#                     format(levels[6], ".1e")])
plt.xlabel('Distancia dirección del viento [m]', fontsize = 'x-large')
plt.ylabel('Distancia perp dir del viento [m]',fontsize = 'x-large')
paso = 'Concentración Max  {0:.2e}  g/m\u00b3'.format(Conc_con.max())
plt.annotate(paso, xy=(u*T/2, lim/f_e_y*.75),fontsize = 'x-large')


plt.subplot(324)

T = 150  #s

Conc_con =(
        q / (8 * (3.14 * T)**(3/2) * (K_x * K_y * K_z)**(1/2))
        * np.exp(-(X-u*T)**2 /(4*K_x*T))
        * np.exp(-(Y - 0)**2 /(4*K_y*T))
        * np.exp(-(zr- 0)**2 /(4*K_z*T))
        )

cmap = mat_co.ListedColormap(['white','LightBlue','Deepskyblue','SpringGreen', 'yellow','orange', 'red']) #selecciono los colores
ccmi = 10**int(np.log10(1E-5*Conc_con.max()))
ccma = 10**int(np.log10(Conc_con.max()))
if (ccmi == 0.0001):
#    levels = [ccmi,ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma*5,ccma*10]
    levels = [ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma*5,ccma*10]
else:
#    levels = [ccmi,ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma,ccma*10]
    levels = [ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma,ccma*10]


CS = plt.contourf(X,Y,Conc_con,levels, cmap = cmap,norm=norm)#colors='k')#, linewidths=.5, linestyles=None)
CS1 = plt.contour(X,Y,Conc_con,levels)#colors='k')#, linewidths=.5, linestyles=None)
cbar = plt.colorbar(CS, boundaries=levels)
cbar.ax.set_title('Concentración')
cbar.set_ticklabels([format(levels[0], ".1e"),
                     format(levels[1], ".1e"),
                     format(levels[2], ".1e"),
                     format(levels[3], ".1e"),
                     format(levels[4], ".1e"),
                     format(levels[5], ".1e")])#,
#                     format(levels[6], ".1e")])

plt.xlabel('Distancia dirección del viento [m]', fontsize = 'x-large')
plt.ylabel('Distancia perp dir del viento [m]',fontsize = 'x-large')
paso = 'Concentración Max  {0:.2e}  g/m\u00b3'.format(Conc_con.max())
plt.annotate(paso, xy=(u*T/2, lim/f_e_y*.75),fontsize = 'x-large')

#plt.show()

######################################################################################################    
#plt.subplots(nrows=1, ncols=2, figsize=(22, 6.5), sharey=True)
#-----------------------------------------------------------------------------------------------------
plt.subplot(325)
T = 250 #s

Conc_con =(
        q / (8 * (3.14 * T)**(3/2) * (K_x * K_y * K_z)**(1/2))
        * np.exp(-(X-u*T)**2 /(4*K_x*T))
        * np.exp(-(Y - 0)**2 /(4*K_y*T))
        * np.exp(-(zr- 0)**2 /(4*K_z*T))
        )

cmap = mat_co.ListedColormap(['white','LightBlue','Deepskyblue','SpringGreen', 'yellow','orange', 'red']) #selecciono los colores
ccmi = 10**int(np.log10(1E-5*Conc_con.max()))
ccma = 10**int(np.log10(Conc_con.max()))
if (ccmi == 0.0001):
#    levels = [ccmi,ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma*5,ccma*10]
    levels = [ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma*5,ccma*10]
else:
#    levels = [ccmi,ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma,ccma*10]
    levels = [ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma,ccma*10]


CS = plt.contourf(X,Y,Conc_con,levels, cmap = cmap,norm=norm)#colors='k')#, linewidths=.5, linestyles=None)
CS1 = plt.contour(X,Y,Conc_con,levels)#colors='k')#, linewidths=.5, linestyles=None)
cbar = plt.colorbar(CS, boundaries=levels)
cbar.ax.set_title('Concentración')
cbar.set_ticklabels([format(levels[0], ".1e"),
                     format(levels[1], ".1e"),
                     format(levels[2], ".1e"),
                     format(levels[3], ".1e"),
                     format(levels[4], ".1e"),
                     format(levels[5], ".1e")])#,
#                     format(levels[6], ".1e")])
plt.xlabel('Distancia dirección del viento [m]', fontsize = 'x-large')
plt.ylabel('Distancia perp dir del viento [m]',fontsize = 'x-large')
paso = 'Concentración Max  {0:.2e}  g/m\u00b3'.format(Conc_con.max())
plt.annotate(paso, xy=(u*T/2, lim/f_e_y*.75),fontsize = 'x-large')


plt.subplot(326)

T = 500  #s

Conc_con =(
        q / (8 * (3.14 * T)**(3/2) * (K_x * K_y * K_z)**(1/2))
        * np.exp(-(X-u*T)**2 /(4*K_x*T))
        * np.exp(-(Y - 0)**2 /(4*K_y*T))
        * np.exp(-(zr- 0)**2 /(4*K_z*T))
        )

cmap = mat_co.ListedColormap(['white','LightBlue','Deepskyblue','SpringGreen', 'yellow','orange', 'red']) #selecciono los colores
ccmi = 10**int(np.log10(1E-5*Conc_con.max()))
ccma = 10**int(np.log10(Conc_con.max()))
if (ccmi == 0.0001):
#    levels = [ccmi,ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma*5,ccma*10]
    levels = [ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma*5,ccma*10]
else:
#    levels = [ccmi,ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma,ccma*10]
    levels = [ccmi*10,ccmi*100,ccmi*1000,ccmi*1E4,ccma,ccma*10]


CS = plt.contourf(X,Y,Conc_con,levels, cmap = cmap,norm=norm)#colors='k')#, linewidths=.5, linestyles=None)
CS1 = plt.contour(X,Y,Conc_con,levels)#colors='k')#, linewidths=.5, linestyles=None)
cbar = plt.colorbar(CS, boundaries=levels)
cbar.ax.set_title('Concentración')
cbar.set_ticklabels([format(levels[0], ".1e"),
                     format(levels[1], ".1e"),
                     format(levels[2], ".1e"),
                     format(levels[3], ".1e"),
                     format(levels[4], ".1e"),
                     format(levels[5], ".1e")])#,
#                     format(levels[6], ".1e")])

plt.xlabel('Distancia dirección del viento [m]', fontsize = 'x-large')
plt.ylabel('Distancia perp dir del viento [m]',fontsize = 'x-large')
paso = 'Concentración Max  {0:.2e}  g/m\u00b3'.format(Conc_con.max())
plt.annotate(paso, xy=(u*T/2, lim/f_e_y*.75),fontsize = 'x-large')

st.pyplot(plt.gcf())   
