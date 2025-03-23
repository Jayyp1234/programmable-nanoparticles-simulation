import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🌡️ Nanoparticle Temperature Response (Refined Model, Mahmoud et al., 2017 Aligned)")

# Temperature slider
temperature = st.slider('Temperature (°C)', 60, 150, 90)

# Constants (Refined)
D0 = 50  # nm
kT = 0.002  # lower swelling constant for temperature response
alpha = 0.015  # viscosity reduction sensitivity
beta = 0.01  # rheology sensitivity factor for diameter effect

# Rheology constants (Herschel–Bulkley model)
tau_y_base = 5
K_base = 0.02
n = 0.7

# Current diameter calculation
D = D0 * (1 + kT * (temperature - 90))
diameter_change_percent = ((D - D0) / D0) * 100

# Exponential viscosity reduction, aligned with Mahmoud et al., 2017
K = K_base * np.exp(-alpha * (temperature - 90))

# Rheology simulation for multiple temperatures
temps = [60, 90, 120, 150]
shear_rate = np.linspace(1, 200, 100)

fig, ax = plt.subplots()

for temp in temps:
    D_temp = D0 * (1 + kT * (temp - 90))
    K_temp = K_base * np.exp(-alpha * (temp - 90))
    tau_y = tau_y_base
    tau = tau_y + K_temp * shear_rate**n * (1 + beta * (D_temp - D0))
    
    ax.plot(shear_rate, tau, label=f"{temp}°C")

ax.set_title('Rheology: Temperature Response (Refined)')
ax.set_xlabel('Shear Rate (1/s)')
ax.set_ylabel('Shear Stress (Pa)')
ax.legend()
st.pyplot(fig)

# Calculate viscosity change percentage relative to baseline (90°C)
baseline_K = K_base * np.exp(-alpha * (90 - 90))
current_K = K_base * np.exp(-alpha * (temperature - 90))
viscosity_change_percent = ((current_K - baseline_K) / baseline_K) * 100

# Display metrics side-by-side
col1, col2 = st.columns(2)
col1.metric("NP Diameter (nm)", f"{D:.2f} nm", f"{diameter_change_percent:+.2f}%")
col2.metric("Viscosity Change (%)", f"{viscosity_change_percent:.2f}%")

# Observations
st.markdown("""
#### 🔎 Observations:
- As temperature increases, **shear stress decreases** due to lower viscosity, which aligns with Mahmoud et al., 2017.
- Nanoparticle swelling helps maintain stability despite reduced viscosity.
""")
