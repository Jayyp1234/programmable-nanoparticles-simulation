import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("⚙️ Nanoparticle Pressure Response Only")

# Pressure slider
pressure = st.slider('Pressure (psi)', 2000, 15000, 5000)

# Constants (adapted from Gerogiorgis et al., 2017)
D0, kP = 50, 0.015  
D = D0 * (1 + kP * (pressure - 5000) / 10000)

# Rheology calculation (pressure-induced gelation)
shear_rate = np.linspace(1, 200, 100)
tau_y_base, K, n, beta = 5, 0.02, 0.7, 0.01
tau_y = tau_y_base * (1 + beta * (D - D0))
tau = tau_y + K * shear_rate**n

# Plot
fig, ax = plt.subplots()
ax.plot(shear_rate, tau, label=f"{pressure} psi")
ax.set_title('Rheology: Pressure Response Only')
ax.set_xlabel('Shear Rate (1/s)')
ax.set_ylabel('Shear Stress (Pa)')
ax.legend()
st.pyplot(fig)

# % Change Calculation
yield_stress_change_percent = ((tau_y - tau_y_base) / tau_y_base) * 100
st.metric("Yield Stress Change (%)", f"{yield_stress_change_percent:.2f}%")
