import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🔬 smFRET Time Trajectory Simulator")

# ==========================
# Sidebar Parameters
# ==========================

st.sidebar.header("Molecular States")

E_low = st.sidebar.slider("Low FRET state", 0.1, 0.5, 0.3)
E_high = st.sidebar.slider("High FRET state", 0.5, 0.9, 0.7)

k_open = st.sidebar.slider("Transition rate open→closed (Hz)", 0.1, 10.0, 2.0)
k_close = st.sidebar.slider("Transition rate closed→open (Hz)", 0.1, 10.0, 1.0)

st.sidebar.header("Photon Simulation")

photon_rate = st.sidebar.slider("Photon count rate", 100, 2000, 800)
bleach_time = st.sidebar.slider("Bleaching time (s)", 1.0, 10.0, 5.0)

total_time = st.sidebar.slider("Total acquisition time (s)", 2.0, 20.0, 10.0)
dt = 0.01

# ==========================
# Time axis
# ==========================

time = np.arange(0, total_time, dt)
n = len(time)

# ==========================
# Generate Markov switching
# ==========================

state = np.zeros(n)
state[0] = 0  # start in low state

for i in range(1, n):

    if state[i-1] == 0:
        if np.random.rand() < k_open * dt:
            state[i] = 1
        else:
            state[i] = 0

    else:
        if np.random.rand() < k_close * dt:
            state[i] = 0
        else:
            state[i] = 1

# ==========================
# Assign FRET efficiency
# ==========================

E = np.where(state == 0, E_low, E_high)

# ==========================
# Simulate bleaching
# ==========================

bleach_index = int(bleach_time / dt)

photon_total = np.ones(n) * photon_rate
photon_total[bleach_index:] = 0

# ==========================
# Photon shot noise
# ==========================

IA = np.random.poisson(photon_total * E * dt)
ID = np.random.poisson(photon_total * (1 - E) * dt)

# Avoid division zero
FRET = IA / (IA + ID + 1e-9)

# ==========================
# Plot Trajectories
# ==========================

st.subheader("📈 smFRET Time Trajectory")

fig, ax = plt.subplots(3,1, figsize=(10,7), sharex=True)

ax[0].plot(time, ID, label="Donor")
ax[0].plot(time, IA, label="Acceptor")
ax[0].set_ylabel("Photon counts")
ax[0].legend()

ax[1].plot(time, FRET, color="purple")
ax[1].set_ylabel("FRET Efficiency")
ax[1].set_ylim(0,1)

ax[2].plot(time, state)
ax[2].set_ylabel("State")
ax[2].set_xlabel("Time (s)")

st.pyplot(fig)

# ==========================
# Histogram FRET
# ==========================

st.subheader("📊 FRET Histogram")

fig2, ax2 = plt.subplots()

ax2.hist(FRET[FRET > 0], bins=40)
ax2.set_xlabel("FRET Efficiency")

st.pyplot(fig2)

# ==========================
# Explanation
# ==========================

st.markdown("""
### 🔬 Interpretation

✔ State switching produces discrete FRET levels  
✔ Photon shot noise causes fluctuations  
✔ Bleaching causes signal disappearance  

This mimics real single-molecule experiments.
""")
