import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve

st.set_page_config(layout="wide")
st.title("🔬 Confocal Insight Lab")

# =========================
# Sidebar Controls
# =========================

st.sidebar.header("Optical Parameters")

NA = st.sidebar.slider("Numerical Aperture", 0.5, 1.4, 1.0)
wavelength = st.sidebar.slider("Wavelength (nm)", 400, 700, 520)

# =========================
# Grid
# =========================

size = 64
x = np.linspace(-2, 2, size)
y = np.linspace(-2, 2, size)
z = np.linspace(-2, 2, size)

X, Y, Z = np.meshgrid(x, y, z)

# =========================
# Synthetic Sample
# =========================

sphere = np.exp(-(X**2 + Y**2 + Z**2))
filament = np.exp(-(X**2 + (Y - 0.8)**2 + Z**2) * 4)

sample = sphere + filament

# =========================
# PSF Model
# =========================

#sigma_xy = wavelength / (NA * 1000)
#sigma_z = 2 * sigma_xy

#PSF = np.exp(-(X**2 + Y**2)/(2*sigma_xy**2) - (Z**2)/(2*sigma_z**2))
#PSF /= PSF.sum()

#PSF_confocal = PSF**2
#PSF_confocal /= PSF_confocal.sum()
# =========================
# PSF Model (Improved)
# =========================

sigma_xy = wavelength / (NA * 1000)
sigma_z = 2.5 * sigma_xy   # widefield axial blur

PSF = np.exp(-(X**2 + Y**2)/(2*sigma_xy**2) - (Z**2)/(2*sigma_z**2))
PSF /= PSF.max()
# ---- Confocal PSF ----

PSF_confocal = PSF**2
# Axial narrowing boost (important)
PSF_confocal = np.exp(-(X**2 + Y**2)/(2*(sigma_xy/np.sqrt(2))**2)
                      - (Z**2)/(2*(sigma_z/2)**2))

PSF_confocal /= PSF_confocal.max()
# =========================
# Imaging Simulation
# =========================

widefield = fftconvolve(sample, PSF, mode="same")
confocal = fftconvolve(sample, PSF_confocal, mode="same")

widefield /= widefield.max()
confocal /= confocal.max()

# =========================
# Slice Controls
# =========================

z_idx = st.slider("Z slice", 0, size-1, size//2)
y_idx = st.slider("Y slice", 0, size-1, size//2)
x_idx = st.slider("X slice", 0, size-1, size//2)

# =========================
# Orthogonal Viewer
# =========================

st.subheader("🧭 Orthogonal Viewer")

col1, col2 = st.columns(2)

with col1:
    st.write("Widefield")

    fig, ax = plt.subplots(1,3, figsize=(10,3))

    ax[0].imshow(widefield[:,:,z_idx], cmap="hot")
    ax[0].set_title("XY")

    ax[1].imshow(widefield[:,y_idx,:], cmap="hot")
    ax[1].set_title("XZ")

    ax[2].imshow(widefield[x_idx,:,:], cmap="hot")
    ax[2].set_title("YZ")

    st.pyplot(fig)

with col2:
    st.write("Confocal")

    fig, ax = plt.subplots(1,3, figsize=(10,3))

    ax[0].imshow(confocal[:,:,z_idx], cmap="hot")
    ax[0].set_title("XY")

    ax[1].imshow(confocal[:,y_idx,:], cmap="hot")
    ax[1].set_title("XZ")

    ax[2].imshow(confocal[x_idx,:,:], cmap="hot")
    ax[2].set_title("YZ")

    st.pyplot(fig)

# =========================
# Line Profile Analyzer
# =========================

st.subheader("📏 Line Profile Resolution")

line_y = st.slider("Line Y position", 0, size-1, size//2)

profile_w = widefield[:, line_y, z_idx]
profile_c = confocal[:, line_y, z_idx]

fig2, ax2 = plt.subplots()

ax2.plot(profile_w, label="Widefield")
ax2.plot(profile_c, label="Confocal")
ax2.set_xlabel("Distance")
ax2.set_ylabel("Intensity")
ax2.legend()

st.pyplot(fig2)

# =========================
# Explanation
# =========================
def fwhm(signal):
    half_max = np.max(signal) / 2
    indices = np.where(signal >= half_max)[0]
    return indices[-1] - indices[0] if len(indices) > 1 else 0

fwhm_w = fwhm(profile_w)
fwhm_c = fwhm(profile_c)

st.write(f"Widefield FWHM: {fwhm_w}")
st.write(f"Confocal FWHM: {fwhm_c}")

st.markdown("""
### 🔬 Interpretation Guide

✔ Orthogonal viewer shows axial blur difference  
✔ Confocal slices appear thinner in XZ / YZ  

✔ Line profile:
- Widefield → broader peak  
- Confocal → sharper peak  

This demonstrates improved optical sectioning and resolution.
""")
