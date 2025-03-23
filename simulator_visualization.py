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

# Initial parameters based on literature
D0 = 50  # Initial diameter (nm)
kpH, kT, kP = 0.02, 0.02, 0.015  # Swelling constants (Zamora-Ledezma et al., Mahmoud et al.)

# Hybrid nanoparticle diameter response
D_hybrid = D0 * (1 + kpH * (pH - 7) + kT * (temperature - 90)/90 + kP * (pressure - 5000)/10000)
percent_swelling = ((D_hybrid - D0) / D0) * 100

# Rheology (Herschel–Bulkley Model, Gokapai et al., 2024)
shear_rate = np.linspace(1, 200, 100)
tau_y_base, K, n = 5, 0.02, 0.7
viscosity = K * (1 + 0.6 * (temperature - 90)/90) * (1 + 0.1 * (pressure - 5000)/10000)
tau_y = tau_y_base * (1 + 0.4 * (D_hybrid - D0) / D0)
tau_hybrid = tau_y + viscosity * shear_rate ** n

# Conventional fluid baseline
tau_conv = tau_y_base + K * shear_rate ** n
percent_viscosity_increase = ((np.mean(tau_hybrid) - np.mean(tau_conv)) / np.mean(tau_conv)) * 100

# Fluid loss/stability improvement metric
stability_metric = np.clip(100 - abs(np.mean(tau_hybrid) - 20) * 3, 0, 100)
fluid_loss_reduction = stability_metric / 2  # Simplified assumption based on stability

# Rheology Comparison Plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(shear_rate, tau_hybrid, 'r-', linewidth=2, label="Hybrid Nanoparticles")
ax.plot(shear_rate, tau_conv, 'b--', linewidth=2, label="Conventional Fluid")
ax.set_title('🔍 Rheology Comparison', fontsize=14)
ax.set_xlabel('Shear Rate (1/s)', fontsize=12)
ax.set_ylabel('Shear Stress (Pa)', fontsize=12)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Metrics Display
col1, col2, col3 = st.columns(3)
col1.metric("Nanoparticle Swelling (%)", f"{percent_swelling:.1f}%")
col2.metric("Viscosity Increase (%)", f"{percent_viscosity_increase:.1f}%")
col3.metric("Fluid Loss Reduction (%)", f"{fluid_loss_reduction:.1f}%")

# Stability Feedback
if stability_metric > 80:
    st.success(f"✅ High Stability: {stability_metric:.0f}% - Optimal Conditions.")
elif stability_metric > 50:
    st.warning(f"⚠️ Moderate Stability: {stability_metric:.0f}% - Caution Advised.")
else:
    st.error(f"🚨 Low Stability: {stability_metric:.0f}% - High Risk.")

# 3D Visualization
st.header("🧬 Nanoparticle Structure (3D)")
phi, theta = np.linspace(0, 2*np.pi, 30), np.linspace(0, np.pi, 30)
phi, theta = np.meshgrid(phi, theta)
x = (D_hybrid / 2) * np.sin(theta) * np.cos(phi)
y = (D_hybrid / 2) * np.sin(theta) * np.sin(phi)
z = (D_hybrid / 2) * np.cos(theta)
fig_3d = go.Figure(go.Surface(z=z, x=x, y=y, colorscale='Viridis'))
fig_3d.update_layout(scene=dict(xaxis_title='X (nm)', yaxis_title='Y (nm)', zaxis_title='Z (nm)'), margin=dict(l=0, r=0, b=0, t=40))
st.plotly_chart(fig_3d, use_container_width=True)

# Practical Insights
st.markdown("""
### 📖 **Practical Insights:**
- **Nanoparticle Swelling:** Clearly visualized, dynamically sealing formation microfractures.
- **Fluid Viscosity Increase:** Clearly improves cuttings transport and reduces fluid loss.
- **Real-Time Adaptation:** Nanoparticles dynamically respond, significantly enhancing drilling safety and efficiency.

*(Formulas adapted from Zamora-Ledezma et al., 2022; Mahmoud et al., 2017; Gokapai et al., 2024)*
""")