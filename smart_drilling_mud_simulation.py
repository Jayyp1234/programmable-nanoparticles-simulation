# smart_drilling_mud_simulation.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -------------------------------
# ENVIRONMENTAL PARAMETERS MODULE
# -------------------------------

class Environment:
    def __init__(self, depth, pressure, temperature, pH):
        self.depth = depth
        self.pressure = pressure
        self.temperature = temperature
        self.pH = pH

# -------------------------------
# NANOPARTICLE KINETICS MODULE
# -------------------------------

class Nanoparticle:
    def __init__(self, rate_constant=0.05, ref_temp=80, max_expansion=1.4):
        self.k = rate_constant
        self.T_ref = ref_temp
        self.S_max = max_expansion

    def kinetics(self, S, t, T):
        """Swelling rate as function of temperature"""
        dSdt = self.k * (T - self.T_ref) * (1 - S / self.S_max)
        return dSdt

# -------------------------------
# FLUID RHEOLOGY MODEL MODULE
# -------------------------------

class FluidRheology:
    def __init__(self, base_yield_stress=50, consistency_index=0.1, flow_behavior_index=0.8):
        self.base_yield_stress = base_yield_stress  # τ₀
        self.consistency_index = consistency_index  # k
        self.flow_behavior_index = flow_behavior_index  # n

    def yield_stress(self, nanoparticle_state, influence_coefficient=20):
        """Adjust yield stress based on nanoparticle state (swelling/expansion)"""
        return self.base_yield_stress + influence_coefficient * (nanoparticle_state - 1.0)

    def shear_stress(self, shear_rate, nanoparticle_state):
        """Herschel-Bulkley shear stress model"""
        τ_y = self.yield_stress(nanoparticle_state)
        τ = τ_y + self.consistency_index * (shear_rate ** self.flow_behavior_index)
        return τ

# -------------------------------
# SIMULATION CORE MODULE
# -------------------------------

def run_simulation(env, np_model, rheology_model, total_time=100, time_steps=500):
    time = np.linspace(0, total_time, time_steps)

    # Initial NP state
    S0 = 1.0

    # Integrate nanoparticle kinetics over time
    S_t = odeint(np_model.kinetics, S0, time, args=(env.temperature,))

    # Calculate yield stress over time
    yield_stress_t = [rheology_model.yield_stress(S[0]) for S in S_t]

    return time, S_t.flatten(), yield_stress_t

# -------------------------------
# VISUALIZATION MODULE
# -------------------------------

def visualize_results(time, np_state, yield_stress):
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(time, np_state, 'b-', marker='o')
    plt.title("Nanoparticle Expansion Over Time")
    plt.xlabel("Time (min)")
    plt.ylabel("Expansion Factor (S)")

    plt.subplot(1, 2, 2)
    plt.plot(time, yield_stress, 'r-', marker='x')
    plt.title("Yield Stress Evolution")
    plt.xlabel("Time (min)")
    plt.ylabel("Yield Stress (Pa)")

    plt.tight_layout()
    plt.show()

# -------------------------------
# MAIN EXECUTION
# -------------------------------

if __name__ == "__main__":
    # Initialize environment (example parameters)
    environment = Environment(depth=3000, pressure=4500, temperature=120, pH=7)

    # Create nanoparticle and fluid rheology models
    nanoparticle_model = Nanoparticle(rate_constant=0.05, ref_temp=80, max_expansion=1.4)
    rheology_model = FluidRheology(base_yield_stress=50, consistency_index=0.1, flow_behavior_index=0.8)

    # Run simulation
    time, np_state, yield_stress = run_simulation(environment, nanoparticle_model, rheology_model)

    # Visualize results
    visualize_results(time, np_state, yield_stress)
