# Description: Smart Hybrid Nanoparticle Drilling Fluid Simulator (Multi-Stimuli)
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Title
st.title("🚀 Smart Hybrid Nanoparticle Drilling Fluid Simulator (Multi-Stimuli)")

st.markdown("""
**Simulating how hybrid nanoparticles respond dynamically to pressure, temperature, and pH variations in downhole environments.**
""")

# Sidebar Input
st.sidebar.header("🔧 Adjust Downhole Conditions")
pressure = st.sidebar.slider('Pressure (psi)', 2000, 15000, 5000)
temperature = st.sidebar.slider('Temperature (°C)', 50, 200, 90)
pH = st.sidebar.slider('pH Level', 4.0, 12.0, 7.0)

# =======================
# Constants for Multi-Stimuli Hybrid NP System
# =======================
D0 = 50  # Initial Diameter in nm
kpH = 0.02     # Zamora-Ledezma et al., 2022
kT = 0.002     # Mahmoud et al., 2017
kP = -0.0015   # Gerogiorgis et al., 2017

# =======================
# Nanoparticle Diameter Calculation (Individual and Hybrid)
# =======================
D_pH = D0 * (1 + kpH * (pH - 7))
D_T = D0 * (1 + kT * (temperature - 90))
D_P = D0 * (1 + kP * (pressure - 5000) / 10000)

# Hybrid response (multiplicative)
D_hybrid = D0 * (1 + kpH * (pH - 7)) * (1 + kT * (temperature - 90)) * (1 + kP * (pressure - 5000) / 10000)

# % Change in NP diameter from baseline
diameter_change_percent = ((D_hybrid - D0) / D0) * 100

# =======================
# Rheological Behavior Calculation (Modified Herschel-Bulkley)
# =======================
shear_rate = np.linspace(1, 200, 100)

tau_y_base = 5  # Pa
K_base = 0.02
n = 0.7

# Viscosity modification
alpha_T = 0.015
alpha_P = 0.01

K_hybrid = K_base * np.exp(-alpha_T * (temperature - 90)) * (1 + alpha_P * (pressure - 5000) / 10000)

# Yield stress increases due to densification (diameter effect)
beta_D = 0.4
tau_y_hybrid = tau_y_base * (1 + beta_D * (D_hybrid - D0) / D0)

# Shear stress (Pa)
tau_hybrid = tau_y_hybrid + K_hybrid * shear_rate ** n
tau_conv = tau_y_base + K_base * shear_rate ** n

# =======================
# Viscosity (Apparent) and % Change
# =======================
representative_shear_rate = 100

apparent_viscosity_hybrid_Pa_s = (tau_y_hybrid + K_hybrid * representative_shear_rate ** n) / representative_shear_rate
apparent_viscosity_conventional_Pa_s = (tau_y_base + K_base * representative_shear_rate ** n) / representative_shear_rate

apparent_viscosity_hybrid_cp = apparent_viscosity_hybrid_Pa_s * 1000
apparent_viscosity_conventional_cp = apparent_viscosity_conventional_Pa_s * 1000

# % Change in viscosity relative to conventional fluid
viscosity_change_percent_cp = ((apparent_viscosity_hybrid_cp - apparent_viscosity_conventional_cp) / apparent_viscosity_conventional_cp) * 100

# =======================
# Stability and Fluid Loss Reduction
# =======================
viscosity_avg = np.mean(tau_hybrid)
stability = np.clip(100 - abs(viscosity_avg - 20) * 3, 0, 100)

fluid_loss_reduction = np.clip(30 + (diameter_change_percent * 0.5) + (stability * 0.2), 0, 60)

# =======================
# Rheology Plot
# =======================
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(shear_rate, tau_hybrid, 'r-', linewidth=2, label="Hybrid Nanoparticles")
ax.plot(shear_rate, tau_conv, 'b--', linewidth=2, label="Conventional Fluid")
ax.set_title('Rheology Comparison (Hybrid vs Conventional)', fontsize=14)
ax.set_xlabel('Shear Rate (1/s)', fontsize=12)
ax.set_ylabel('Shear Stress (Pa)', fontsize=12)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# =======================
# Display Metrics (With % Change)
# =======================
col1, col2, col3 = st.columns(3)

col1.metric(
    label="NP Diameter",
    value=f"{D_hybrid:.2f} nm",
    delta=f"{diameter_change_percent:+.2f}%",
    help="Change in nanoparticle diameter relative to baseline (50 nm)."
)

col2.metric(
    label="Apparent Viscosity",
    value=f"{apparent_viscosity_hybrid_cp:.2f} cp",
    delta=f"{viscosity_change_percent_cp:+.2f}%",
    delta_color="inverse" if viscosity_change_percent_cp < 0 else "normal",
    help="% change in viscosity relative to conventional fluid."
)

col3.metric(
    label="Fluid Loss Reduction",
    value=f"{fluid_loss_reduction:.2f} %",
    delta=f"Stability {stability:.0f}%",
    help="Estimated % reduction in fluid loss based on diameter and system stability."
)

# =======================
# Stability Feedback
# =======================
if stability > 80:
    st.success(f"✅ High Stability: {stability:.0f}% - Optimal Drilling Conditions.")
elif stability > 50:
    st.warning(f"⚠️ Moderate Stability: {stability:.0f}% - Monitor Fluid Performance.")
else:
    st.error(f"🚨 Low Stability: {stability:.0f}% - High Risk of Fluid Loss and Instability.")

# =======================
# 3D Nanoparticle Visualization
# =======================
st.header("🧬 3D Nanoparticle Structure Visualization")
phi, theta = np.linspace(0, 2*np.pi, 30), np.linspace(0, np.pi, 30)
phi, theta = np.meshgrid(phi, theta)

x = (D_hybrid / 2) * np.sin(theta) * np.cos(phi)
y = (D_hybrid / 2) * np.sin(theta) * np.sin(phi)
z = (D_hybrid / 2) * np.cos(theta)

fig_3d = go.Figure(go.Surface(z=z, x=x, y=y, colorscale='Viridis'))
fig_3d.update_layout(scene=dict(xaxis_title='X (nm)', yaxis_title='Y (nm)', zaxis_title='Z (nm)'),
                     margin=dict(l=0, r=0, b=0, t=40))
st.plotly_chart(fig_3d, use_container_width=True)

# =======================
# Detailed Property Comparison
# =======================
if st.checkbox("🔖 Show Detailed Property Comparison"):
    comparison_table = {
        "Property": ["Max Shear Stress (Pa)", "Yield Stress (Pa)", "Consistency Index (K)", "NP Diameter (nm)"],
        "Hybrid Fluid": [f"{tau_hybrid.max():.2f}", f"{tau_y_hybrid:.2f}", f"{K_hybrid:.4f}", f"{D_hybrid:.2f}"],
        "Conventional Fluid": [f"{tau_conv.max():.2f}", f"{tau_y_base:.2f}", f"{K_base:.4f}", "N/A"]
    }
    st.table(comparison_table)

# =======================
# Practical Insights
# =======================
st.markdown("""
### 📖 **Practical Insights**
- **Nanoparticle Swelling and Shrinkage:** Dynamically seals microfractures, enhancing wellbore integrity.
- **Thermo-Responsive Viscosity Control:** Ensures efficient cuttings transport and reduces excessive thinning at elevated temperatures.
- **Pressure-Activated Gelation:** Increases yield stress and stabilizes borehole walls under high-pressure conditions.
- **Multi-Stimuli Hybrid Nanoparticles:** Offer superior performance over conventional and single-stimulus systems.

📚 *Models informed by Zamora-Ledezma et al., 2022; Mahmoud et al., 2017; Gerogiorgis et al., 2017; Gokapai et al., 2024.*
""")
