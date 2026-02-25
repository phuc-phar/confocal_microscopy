import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

st.set_page_config(page_title="Improved Confocal Simulator")

# ======================================================
# Create realistic 3D sample with multiple layers
# ======================================================
def generate_sample(size=120):

    x = np.linspace(-6, 6, size)
    y = np.linspace(-6, 6, size)
    z = np.linspace(-6, 6, size)

    X, Y, Z = np.meshgrid(x, y, z)

    # Multiple objects at different Z
    obj1 = np.exp(-(X**2 + Y**2 + (Z-2)**2))
    obj2 = np.exp(-((X-2)**2 + (Y+2)**2 + (Z+2)**2))

    return obj1 + obj2


sample = generate_sample()

size = sample.shape[0]
z_coords = np.linspace(-6, 6, size)

# ======================================================
# Axial PSF model (controls optical sectioning)
# ======================================================
def axial_psf(z, z0, width):

    return np.exp(-(z-z0)**2 / (2*width**2))


# ======================================================
# Widefield vs Confocal
# ======================================================
def compare():

    st.header("🔬 Widefield vs Confocal (Improved Physics)")

    z_index = st.slider("Focus Z plane", 0, size-1, size//2)
    pinhole = st.slider("Pinhole Size (AU)", 0.3, 3.0, 1.0)

    z0 = z_coords[z_index]

    # ------------------------
    # Widefield simulation
    # ------------------------
    widefield = np.zeros((size, size))

    for i, z in enumerate(z_coords):
        # Out-of-focus blur increases with distance
        blur_strength = abs(z - z0) * 2 + 1
        blurred = gaussian_filter(sample[:, :, i], sigma=blur_strength)
        widefield += blurred

    # ------------------------
    # Confocal simulation
    # ------------------------
    confocal = np.zeros((size, size))

    # Axial detection PSF width depends on pinhole
    psf_width = pinhole * 1.2

    for i, z in enumerate(z_coords):
        weight = axial_psf(z, z0, psf_width)
        confocal += sample[:, :, i] * weight

    # Confocal still has small blur
    confocal = gaussian_filter(confocal, sigma=1)

    # Normalize
    widefield /= np.max(widefield)
    confocal /= np.max(confocal)

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots()
        ax1.imshow(widefield, cmap="inferno")
        ax1.set_title("Widefield")
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots()
        ax2.imshow(confocal, cmap="inferno")
        ax2.set_title("Confocal")
        st.pyplot(fig2)


# ======================================================
# Z stack visualization
# ======================================================
def z_stack():

    st.header("🧬 Z Plane Visualization")

    z_index = st.slider("Z plane", 0, size-1, size//2)

    fig, ax = plt.subplots()
    ax.imshow(sample[:, :, z_index], cmap="inferno")
    ax.set_title("True Optical Slice")

    st.pyplot(fig)


# ======================================================
# MAIN
# ======================================================
st.title("🔬 Confocal Optical Sectioning Simulator")

menu = st.sidebar.selectbox(
    "Select Simulation",
    ["Widefield vs Confocal", "Z Plane Slice"]
)

if menu == "Widefield vs Confocal":
    compare()

if menu == "Z Plane Slice":
    z_stack()
