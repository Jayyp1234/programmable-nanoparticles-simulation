import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
shear_rate = np.linspace(1, 200, 100)
D0 = 50  # Initial diameter (nm)
tau_y_base, K, n, beta = 5, 0.02, 0.7, 0.01

# Define single stimuli responses clearly based on literature
# pH-sensitive (Zamora-Ledezma et al., 2022)
def nanoparticle_pH(pH):
    kpH = 0.02
    return D0 * (1 + kpH * (pH - 7))

# Thermo-responsive (Mahmoud et al., 2017)
def nanoparticle_temp(temp):
    kT = 0.02
    return D0 * (1 + kT * (temp - 90)/90)

# Pressure-activated (Gerogiorgis et al., 2017)
def nanoparticle_pressure(pressure):
    kP = 0.015
    return D0 * (1 + kP * (pressure - 5000)/10000)

# Rheology function
def rheology(D):
    tau_y = tau_y_base * (1 + 0.4 * (D - D0) / D0)
    tau = tau_y + K * shear_rate ** n * (1 + beta * (D - D0))
    return tau

# Simulate responses
pH_values = [6, 7, 8, 9]
temp_values = [60, 90, 120, 150]
pressure_values = [3000, 5000, 7000, 9000]

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# pH Response
for pH in pH_values:
    D = nanoparticle_pH(pH)
    tau = rheology(D)
    axes[0].plot(shear_rate, tau, label=f'pH {pH}')
axes[0].set_title('Nanoparticle Response to pH Change')
axes[0].set_xlabel('Shear Rate (1/s)')
axes[0].set_ylabel('Shear Stress (Pa)')
axes[0].legend()
axes[0].grid()

# Temperature Response
for temp in temp_values:
    D = nanoparticle_temp(temp)
    tau = rheology(D)
    axes[1].plot(shear_rate, tau, label=f'{temp}°C')
axes[1].set_title('Nanoparticle Response to Temperature Change')
axes[1].set_xlabel('Shear Rate (1/s)')
axes[1].legend()
axes[1].grid()

# Pressure Response
for pressure in pressure_values:
    D = nanoparticle_pressure(pressure)
    tau = rheology(D)
    axes[2].plot(shear_rate, tau, label=f'{pressure} psi')
axes[2].set_title('Nanoparticle Response to Pressure Change')
axes[2].set_xlabel('Shear Rate (1/s)')
axes[2].legend()
axes[2].grid()

plt.tight_layout()
plt.show()