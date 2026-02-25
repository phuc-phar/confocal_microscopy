import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

st.title("🧬 Confocal FRET Simulator")

# ---------------------------------------------------
# Sidebar Parameters
# ---------------------------------------------------

st.sidebar.header("FRET Parameters")

distance = st.sidebar.slider("Donor–Acceptor Distance (nm)", 1, 10, 5)
R0 = st.sidebar.slider("Förster Radius R0 (nm)", 2, 8, 5)
donor_intensity = st.sidebar.slider("Initial Donor Intensity", 0.2, 1.0, 1.0)

# ---------------------------------------------------
# FRET Efficiency Calculation
# ---------------------------------------------------

def fret_efficiency(r, R0):
    return 1 / (1 + (r / R0)**6)

E = fret_efficiency(distance, R0)

st.metric("FRET Efficiency", f"{E:.2f}")

# ---------------------------------------------------
# Generate Synthetic Sample
# ---------------------------------------------------

size = 128
sample = np.zeros((size, size))

for _ in range(6):
    x = np.random.randint(20, size-20)
    y = np.random.randint(20, size-20)
    sample[x-5:x+5, y-5:y+5] = 1

sample = gaussian_filter(sample, 2)

# ---------------------------------------------------
# Simulate Donor and Acceptor Channels
# ---------------------------------------------------

donor_signal = donor_intensity * (1 - E) * sample
acceptor_signal = donor_intensity * E * sample

donor_signal = gaussian_filter(donor_signal, 1)
acceptor_signal = gaussian_filter(acceptor_signal, 1)

# ---------------------------------------------------
# Display Channels
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Donor Channel")
    st.image(donor_signal, clamp=True)

with col2:
    st.subheader("Acceptor Channel")
    st.image(acceptor_signal, clamp=True)

# ---------------------------------------------------
# Overlay Image
# ---------------------------------------------------

overlay = np.zeros((size, size, 3))
overlay[..., 1] = donor_signal     # Green
overlay[..., 0] = acceptor_signal  # Red

st.subheader("Merged FRET Image")
st.image(overlay, clamp=True)

# ---------------------------------------------------
# Line Profile
# ---------------------------------------------------

line = size // 2

fig_lp, ax = plt.subplots()

ax.plot(donor_signal[line, :], label="Donor")
ax.plot(acceptor_signal[line, :], label="Acceptor")

ax.legend()
ax.set_title("Line Profile FRET")

st.pyplot(fig_lp)

# ---------------------------------------------------
# Efficiency vs Distance Plot
# ---------------------------------------------------

r_range = np.linspace(1, 10, 100)
E_curve = fret_efficiency(r_range, R0)

fig_eff, ax = plt.subplots()
ax.plot(r_range, E_curve)
ax.scatter(distance, E, s=80)
ax.set_xlabel("Distance (nm)")
ax.set_ylabel("Efficiency")
ax.set_title("FRET Efficiency Curve")

st.pyplot(fig_eff)

# ---------------------------------------------------
# Educational Explanation
# ---------------------------------------------------

with st.expander("📘 FRET Explanation"):

    st.markdown(f"""
### What is FRET?

FRET = Fluorescence Resonance Energy Transfer

Energy transfers from donor fluorophore to acceptor fluorophore.

---

### Current Simulation

- Distance r = {distance} nm  
- Förster Radius R0 = {R0} nm  
- Efficiency E = {E:.2f}

---

### Biological Meaning

High FRET:
- Molecules are close
- Indicates interaction / conformational change

Low FRET:
- Molecules far apart
- No interaction
""")
