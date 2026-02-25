import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(layout="wide")

st.title("🔬 Confocal Microscope System Designer & Simulator")

# -------------------------------
# Sidebar – System Configuration
# -------------------------------

st.sidebar.header("⚙️ Optical Configuration")

na = st.sidebar.slider("Numerical Aperture (NA)", 0.5, 1.4, 1.2)
wavelength = st.sidebar.slider("Excitation Wavelength (nm)", 400, 700, 488)
pinhole = st.sidebar.slider("Pinhole size (Airy Units)", 0.2, 2.0, 1.0)
z_planes = st.sidebar.slider("Number of Z planes", 5, 40, 20)

# -------------------------------
# Helper Functions
# -------------------------------

def airy_psf(size, na, wavelength, pinhole_factor=1):
    """Simulated PSF (approximation)"""

    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    xx, yy = np.meshgrid(x, y)

    r = np.sqrt(xx**2 + yy**2)

    sigma = wavelength / (na * 800)
    psf = np.exp(-(r**2) / (2 * sigma**2))

    psf = gaussian_filter(psf, pinhole_factor * 2)
    return psf


def generate_sample(size=128):
    """Synthetic biological sample"""

    img = np.zeros((size, size))

    for _ in range(8):
        x = np.random.randint(20, size - 20)
        y = np.random.randint(20, size - 20)
        img[x - 5:x + 5, y - 5:y + 5] = np.random.uniform(0.5, 1.0)

    return gaussian_filter(img, 3)


# -------------------------------
# Optical Path Visualization
# -------------------------------

st.header("🧭 Confocal Optical Path")

st.markdown("""
Laser → Scanner → Objective → Sample → Emission → Pinhole → Detector
""")

fig_path, ax = plt.subplots(figsize=(8, 2))

elements = ["Laser", "Scanner", "Objective", "Sample", "Pinhole", "Detector"]
x = np.arange(len(elements))

ax.scatter(x, np.zeros_like(x), s=200)
for i, label in enumerate(elements):
    ax.text(i, 0.1, label, ha='center')

ax.plot(x, np.zeros_like(x))
ax.axis('off')

st.pyplot(fig_path)

# -------------------------------
# Generate Sample + PSF
# -------------------------------

st.header("🧬 Sample Simulation")

size = 128
sample = generate_sample(size)

psf_confocal = airy_psf(size, na, wavelength, pinhole)
psf_widefield = airy_psf(size, na, wavelength, pinhole_factor=3)

confocal_img = gaussian_filter(sample, 1) * psf_confocal
widefield_img = gaussian_filter(sample, 3) * psf_widefield

col1, col2 = st.columns(2)

with col1:
    st.subheader("Widefield")
    st.image(widefield_img, clamp=True)

with col2:
    st.subheader("Confocal")
    st.image(confocal_img, clamp=True)

# -------------------------------
# Line Profile Comparison
# -------------------------------

st.header("📈 Line Profile Comparison")

line_y = size // 2

fig_lp, ax = plt.subplots()

ax.plot(widefield_img[line_y, :], label="Widefield")
ax.plot(confocal_img[line_y, :], label="Confocal")

ax.legend()
ax.set_title("Signal Intensity Along Line")

st.pyplot(fig_lp)

# -------------------------------
# Z-stack Simulation
# -------------------------------

st.header("📦 Z-stack Simulation")

z_stack = []

for z in range(z_planes):
    blur = gaussian_filter(sample, sigma=z * 0.3)
    z_img = blur * airy_psf(size, na, wavelength, pinhole)
    z_stack.append(z_img)

z_stack = np.array(z_stack)

z_index = st.slider("Select Z plane", 0, z_planes - 1, z_planes // 2)

st.image(z_stack[z_index], clamp=True)

# -------------------------------
# 3D Volume Viewer
# -------------------------------

st.header("🧊 True 3D Volume Viewer")

threshold = st.slider("Intensity Threshold", 0.1, 1.0, 0.4)

coords = np.where(z_stack > threshold)

fig3d = plt.figure(figsize=(6, 6))
ax3d = fig3d.add_subplot(111, projection='3d')

ax3d.scatter(coords[2], coords[1], coords[0], s=1)
ax3d.set_xlabel("X")
ax3d.set_ylabel("Y")
ax3d.set_zlabel("Z")

st.pyplot(fig3d)

# -------------------------------
# Educational Notes
# -------------------------------

with st.expander("📘 Explanation"):

    st.markdown(f"""
### Confocal Principles

- NA = {na}
- Wavelength = {wavelength} nm
- Pinhole = {pinhole} AU

Smaller pinhole:
- ↑ Optical sectioning
- ↓ Signal intensity

Higher NA:
- ↑ Resolution
- ↑ Light collection
""")
