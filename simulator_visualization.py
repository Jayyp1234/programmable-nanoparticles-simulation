import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# App Title
st.title("🚀 Smart Hybrid Nanoparticle Drilling Fluid Simulator")
st.markdown("""
**Interactive visualization demonstrating how hybrid nanoparticles dynamically respond to downhole conditions (Pressure, Temperature, pH).**

Adjust conditions to observe nanoparticle swelling, fluid viscosity changes, and their impact on wellbore stability.
""")

# Sidebar: Interactive Controls
st.sidebar.header("🔧 Adjust Downhole Conditions")
pressure = st.sidebar.slider('Pressure (psi)', 2000, 15000, 5000)
temperature = st.sidebar.slider('Temperature (°C)', 50, 200, 90)
pH = st.sidebar.slider('pH Level', 4.0, 12.0, 7.0)

# Nanoparticle Diameter Calculation (Hybrid Nanoparticles)
# Governing equations based on dual-stimuli response (Zamora-Ledezma et al., 2022; Mahmoud et al., 2017)
D0 = 50  # Initial diameter (nm)
kpH = 0.04    # based on Zamora-Ledezma et al., 2022 swelling constant for pH response (nm/unit pH)
kT = 0.02     # based on Mahmoud et al., 2017 and Borisov et al., 2017 swelling constant for temperature response (nm/°C)
kP = 0.015    # based on Gerogiorgis et al., 2017 and Vryzas et al., 2017 swelling constant for pressure response (nm/psi)


# Diameter change responding naturally to pH, temperature, and pressure
D_hybrid = D0 * (1 + kpH * (pH - 7) + kT * (temperature - 90)/90 + kP * (pressure - 5000)/10000)

# Rheological Behavior Calculation (Modified Herschel–Bulkley Model, Gokapai et al., 2024)
shear_rate = np.linspace(1, 200, 100)
tau_y_base, K, n = 5, 0.02, 0.7

# Yield stress and viscosity influenced naturally by nanoparticle size
viscosity = K * (1 + 0.6 * (temperature - 90)/90) * (1 + 0.1 * (pressure - 5000)/10000)

tau_y = tau_y_base * (1 + 0.4 * (D_hybrid - D0) / D0)
tau_hybrid = tau_y + viscosity * shear_rate ** n

# Conventional fluid without nanoparticle effects (for baseline comparison)
tau_conv = tau_y_base + K * shear_rate ** n

# Plotting Rheology Comparison
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(shear_rate, tau_hybrid, 'r-', linewidth=2, label="Hybrid Nanoparticles")
ax.plot(shear_rate, tau_conv, 'b--', linewidth=2, label="Conventional Fluid")
ax.set_title('Rheology Comparison', fontsize=14)
ax.set_xlabel('Shear Rate (1/s)', fontsize=12)
ax.set_ylabel('Shear Stress (Pa)', fontsize=12)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Stability metric based on practical viscosity
viscosity_avg = np.mean(tau_hybrid)

stability = np.clip(100 - abs(viscosity_avg - 20) * 3, 0, 100)

# Dynamic Metrics Display
col1, col2 = st.columns(2)
col1.metric("Nanoparticle Diameter", f"{D_hybrid:.2f} nm")
col2.metric("Average Fluid Viscosity", f"{viscosity_avg:.2f} cp")

# Stability Feedback
if stability > 80:
    st.success(f"✅ High Stability: {stability:.0f}% - Optimal Drilling Conditions.")
elif stability > 50:
    st.warning(f"⚠️ Moderate Stability: {stability:.0f}% - Caution advised.")
else:
    st.error(f"🚨 Low Stability: {stability:.0f}% - High risk of fluid loss.")

# 3D Visualization of Nanoparticle Structure
st.header("🧬 Nanoparticle Structure (3D)")
phi, theta = np.linspace(0, 2*np.pi, 30), np.linspace(0, np.pi, 30)
phi, theta = np.meshgrid(phi, theta)
x = (D_hybrid / 2) * np.sin(theta) * np.cos(phi)
y = (D_hybrid / 2) * np.sin(theta) * np.sin(phi)
z = (D_hybrid / 2) * np.cos(theta)

fig_3d = go.Figure(go.Surface(z=z, x=x, y=y, colorscale='Viridis'))
fig_3d.update_layout(scene=dict(xaxis_title='X (nm)', yaxis_title='Y (nm)', zaxis_title='Z (nm)'),
                     margin=dict(l=0, r=0, b=0, t=40))
st.plotly_chart(fig_3d, use_container_width=True)

# Detailed Comparison of Fluid Properties
if st.checkbox("🔖 Show Detailed Comparison"):
    comparison_table = {
        "Property": ["Max Shear Stress (Pa)", "Yield Stress (Pa)", "Consistency Index (K)", "Nanoparticle Diameter (nm)"],
        "Hybrid Fluid": [f"{tau_hybrid.max():.2f}", f"{tau_y:.2f}", K, f"{D_hybrid:.2f}"],
        "Conventional Fluid": [f"{tau_conv.max():.2f}", f"{tau_y_base:.2f}", K, "N/A"]
    }
    st.table(comparison_table)
    st.info("🔑 Hybrid fluid dynamically improves viscosity and stability compared to conventional fluids.")

# Practical Explanation
st.markdown("""
### 📖 **Practical Insights:**
- **Nanoparticle Swelling:** Enlarged nanoparticles effectively seal formation microfractures, significantly minimizing fluid invasion and improving wellbore stability.
- **Fluid Viscosity:** Optimal viscosity ensures efficient removal of drill cuttings, reduces fluid loss, and provides consistent protection to formations.
- **Real-Time Adaptation:** Unlike traditional additives, hybrid nanoparticles adjust fluid properties automatically as downhole conditions change, significantly reducing operational risk.

*(Formulas and models adapted from Zamora-Ledezma et al., 2022; Mahmoud et al., 2017; Gokapai et al., 2024)*
""")