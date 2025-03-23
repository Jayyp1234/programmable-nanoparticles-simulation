import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🔬 Nanoparticle pH Response Only")

# pH slider
pH = st.slider('pH Level', 4.0, 12.0, 7.0)

# Constants (based on literature - Zamora-Ledezma et al., 2022)
D0, kpH = 50, 0.04  
D = D0 * (1 + kpH * (pH - 7))

# Rheology calculation (modified Herschel–Bulkley)
shear_rate = np.linspace(1, 200, 100)
tau_y, K, n, beta = 5, 0.02, 0.7, 0.01
tau = tau_y + K * shear_rate**n * (1 + beta * (D - D0))

# Plot
fig, ax = plt.subplots()
ax.plot(shear_rate, tau, label=f"pH {pH}")
ax.set_title('Rheology: pH Response Only')
ax.set_xlabel('Shear Rate (1/s)')
ax.set_ylabel('Shear Stress (Pa)')
ax.legend()
st.pyplot(fig)

# % Change Calculation
size_change_percent = ((D - D0) / D0) * 100
st.metric("NP Size Change (%)", f"{size_change_percent:.2f}%")
