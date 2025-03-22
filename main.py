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

# Interactive Controls
st.sidebar.header("🔧 Adjust Downhole Conditions")
pressure = st.sidebar.slider('Pressure (psi)', 2000, 15000, 5000)
temperature = st.sidebar.slider('Temperature (°C)', 50, 200, 90)
pH = st.sidebar.slider('pH Level', 4.0, 12.0, 7.0)

# Nanoparticle Diameter Calculation (Hybrid)
D0, kpH, kT = 50, 0.015, 0.025
D_hybrid = D0 + kpH * (pH - 7) + kT * (temperature - 90)

# Rheology Calculations
shear_rate = np.linspace(1, 200, 100)
tau_y, K, n, beta = 5, 0.02, 0.7, 0.01
tau_hybrid = tau_y + K * shear_rate**n * (1 + beta * (D_hybrid - D0))
tau_conv = tau_y + K * shear_rate**n

# Plot Rheology Comparison
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(shear_rate, tau_hybrid, 'r-', linewidth=2, label="Hybrid Nanoparticles")
ax.plot(shear_rate, tau_conv, 'b--', linewidth=2, label="Conventional Fluid")
ax.set_title('🔍 Rheology Comparison', fontsize=14)
ax.set_xlabel('Shear Rate (1/s)', fontsize=12)
ax.set_ylabel('Shear Stress (Pa)', fontsize=12)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Practical Stability Metric
viscosity = np.mean(tau_hybrid)
stability = np.clip(100 - abs(viscosity - 20) * 3, 0, 100)

# Dynamic Metrics
col1, col2 = st.columns(2)
col1.metric("Nanoparticle Diameter", f"{D_hybrid:.2f} nm")
col2.metric("Average Fluid Viscosity", f"{viscosity:.2f} cp")

# Stability Alert
if stability > 80:
    st.success(f"✅ High Stability: {stability:.0f}% - Optimal Drilling Conditions.")
elif stability > 50:
    st.warning(f"⚠️ Moderate Stability: {stability:.0f}% - Caution advised.")
else:
    st.error(f"🚨 Low Stability: {stability:.0f}% - High risk of fluid loss.")

# 3D Visualization
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

# Detailed Comparison
toggle = st.checkbox("🔖 Show Detailed Comparison")
if toggle:
    st.table({
        "Property": ["Max Shear Stress (Pa)", "Yield Stress (Pa)", "Consistency Index (K)", "Nanoparticle Diameter (nm)"],
        "Hybrid Fluid": [f"{tau_hybrid.max():.2f}", tau_y, K, f"{D_hybrid:.2f}"],
        "Conventional Fluid": [f"{tau_conv.max():.2f}", tau_y, K, "N/A"]
    })
    st.info("🔑 Hybrid fluid dynamically improves viscosity and stability compared to conventional fluids.")

# Clear Explanations
st.markdown("""
### 📖 **What does this mean practically?**
- **Nanoparticle Swelling:** Larger nanoparticles seal micro-fractures, minimizing fluid loss and enhancing wellbore stability.
- **Fluid Viscosity:** Optimal viscosity ensures efficient cuttings removal and prevents fluid invasion into the formation.
- **Real-Time Adaptation:** Hybrid nanoparticles ensure fluid properties stay within safe, optimal ranges despite changing conditions downhole.
""")
