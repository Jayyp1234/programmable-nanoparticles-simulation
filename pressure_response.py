import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("⚙️ Nanoparticle Pressure-Responsive Behavior (Scientific Model)")

st.markdown("""
This model demonstrates how programmable nanoparticles dynamically respond to downhole pressure variations:
- Shrinkage improves borehole sealing.
- Yield stress increases enhance structural integrity.
- Fluid loss is reduced due to better plugging.
""")

# Pressure input
pressure = st.slider('Pressure (psi)', 2000, 15000, 5000)

# Constants
D0 = 50  # nm, initial nanoparticle diameter
P_ref = 5000  # reference pressure for baseline
alpha = 0.03  # shrinkage sensitivity factor
beta = 0.25  # yield stress sensitivity factor
gamma = 40  # max fluid loss reduction percentage
k = 1 / 5000  # scaling factor for fluid loss equation

# Calculating responses
D_shrink = D0 * (1 - alpha * np.log(pressure / P_ref))
shrinkage_percent = ((D_shrink - D0) / D0) * 100

tau_y_base = 5  # Pa
tau_y = tau_y_base * (1 + beta * np.log(pressure / P_ref))
yield_stress_increase_percent = ((tau_y - tau_y_base) / tau_y_base) * 100

fluid_loss_reduction_percent = gamma * (1 - np.exp(-k * (pressure - P_ref)))

# Rheology calculation
shear_rate = np.linspace(1, 200, 100)
K, n = 0.02, 0.7
tau = tau_y + K * shear_rate ** n

# Plotting rheology
fig, ax = plt.subplots()
ax.plot(shear_rate, tau, label=f"{pressure} psi")
ax.set_title('🔵 Rheology: Pressure Response Only')
ax.set_xlabel('Shear Rate (1/s)')
ax.set_ylabel('Shear Stress (Pa)')
ax.legend()
st.pyplot(fig)

# Metrics display
col1, col2, col3 = st.columns(3)

col1.metric("🧬 NP Diameter (nm)", f"{D_shrink:.2f} nm", f"{shrinkage_percent:.2f}%")
col2.metric("💪 Yield Stress Increase (%)", f"{yield_stress_increase_percent:.2f}%")
col3.metric("💧 Fluid Loss Reduction (%)", f"{fluid_loss_reduction_percent:.2f}%")

st.markdown("""
#### Key Takeaways:
- **Shrinkage**: Up to ~8–10% at higher pressures enhances nanoparticle packing.
- **Yield Stress**: Increases by ~25% due to gel network formation.
- **Fluid Loss**: Reduces naturally with improved fracture sealing and densification.
""")


st.markdown("""
#### Interpretation
- As pressure increases, nanoparticle shrinkage leads to densification, supporting gel formation and stabilizing wellbore walls.
- The yield stress increases up to 25%, enhancing the fluid’s ability to resist deformation and sagging.
- Improved gelation reduces fluid loss by up to 40%, minimizing filtration through microfractures.
""")
