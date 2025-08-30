import numpy as np
import matplotlib.pyplot as plt

# Paramètres du signal d'entrée
A = 1.0
omega = 2 * np.pi / 10
phi = 0

# Paramètres des modules
alpha_EF = 0.5
beta_EF = 0.3

gamma = 0.6
theta_C = 0.5
eta_C = 0.2

zeta = 0.4
lambda_ = 0.1

xi = 0.3
nu = 0.2

mu = 0.5
epsilon = 0.25

# Domaine de simulation
T = 50
dt = 0.1
time = np.arange(0, T, dt)

# Initialisations
I = A * np.sin(omega * time + phi)
tau_EF = np.zeros_like(time)
tau_C = np.zeros_like(time)
tau_JO = np.zeros_like(time)
tau_AG = np.zeros_like(time)
tau_LS = np.zeros_like(time)

# Simulation
for t in range(1, len(time)):
    d_tau_EF = alpha_EF * I[t] - beta_EF * tau_EF[t-1]
    tau_EF[t] = tau_EF[t-1] + d_tau_EF * dt

    d_tau_C = gamma * max(0, tau_EF[t-1] - theta_C) - eta_C * tau_C[t-1]
    tau_C[t] = tau_C[t-1] + d_tau_C * dt

    d_tau_JO = zeta * tau_C[t-1] - lambda_ * tau_JO[t-1]
    tau_JO[t] = tau_JO[t-1] + d_tau_JO * dt

    noise = np.random.normal(0, 0.05)
    d_tau_AG = xi * noise + nu * tau_JO[t-1]
    tau_AG[t] = tau_AG[t-1] + d_tau_AG * dt

    d_tau_LS = mu * ((tau_EF[t-1] + tau_AG[t-1]) - (tau_EF[t-2] + tau_AG[t-2]) if t > 1 else 0) / dt - epsilon * tau_LS[t-1]
    tau_LS[t] = tau_LS[t-1] + d_tau_LS * dt

# Affichage
plt.figure(figsize=(12, 8))
plt.plot(time, tau_EF, label='EchoFuse')
plt.plot(time, tau_C, label='CRITRIX')
plt.plot(time, tau_JO, label='Journal_Oubli')
plt.plot(time, tau_AG, label='AutoGenesisCore')
plt.plot(time, tau_LS, label='LyraScope')
plt.title("Évolution de τc des modules Lyra")
plt.xlabel("Temps")
plt.ylabel("Tension cumulative τc")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
