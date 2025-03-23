import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🌡️ Nanoparticle Temperature Response Only")

# Temperature slider
temperature = st.slider('Temperature (°C)', 50, 200, 90)

# Constants (based on Mahmoud et al., 2017)
D0, kT = 50, 0.01  
D = D0 * (1 + kT * (temperature - 90))

# Rheology calculation
shear_rate = np.linspace(1, 200, 100)
tau_y, K, n, beta = 5, 0.02, 0.7, 0.01
tau = tau_y + K * shear_rate**n * (1 + beta * (D - D0))

# Plot
fig, ax = plt.subplots()
ax.plot(shear_rate, tau, label=f"{temperature} °C")
ax.set_title('Rheology: Temperature Response Only')
ax.set_xlabel('Shear Rate (1/s)')
ax.set_ylabel('Shear Stress (Pa)')
ax.legend()
st.pyplot(fig)

# % Change Calculation
viscosity_change_percent = ((tau.mean() - (tau_y + K * shear_rate**n).mean()) / (tau_y + K * shear_rate**n).mean()) * 100
st.metric("Viscosity Change (%)", f"{viscosity_change_percent:.2f}%")
