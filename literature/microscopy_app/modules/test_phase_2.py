import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Murphy Phase 2 - NA & Resolution")

# =========================
# NA & Acceptance Angle
# =========================
def NA_module():

    st.header("🔬 Numerical Aperture Explorer")

    n = st.slider("Refractive Index (n)", 1.0, 1.52, 1.33)
    NA = st.slider("Numerical Aperture", 0.1, 1.4, 1.2)

    # Acceptance angle
    theta = np.arcsin(NA / n)
    theta_deg = np.degrees(theta)

    st.write(f"Acceptance Angle θ = {theta_deg:.2f}°")

    # Brightness ~ NA^2
    brightness = NA**2
    st.write(f"Relative Brightness ≈ {brightness:.2f}")

    # Plot light collection cone
    fig, ax = plt.subplots()

    r = np.tan(theta)

    ax.plot([0, r], [0, 1])
    ax.plot([0, -r], [0, 1])
    ax.axhline(0)

    ax.set_title("Light Collection Cone")
    ax.set_xlim(-2, 2)
    ax.set_ylim(0, 1.5)

    st.pyplot(fig)


# =========================
# Resolution Calculator
# =========================
def resolution_module():

    st.header("📏 Resolution Calculator")

    wavelength = st.slider("Wavelength (nm)", 400, 700, 520)
    NA = st.slider("NA", 0.2, 1.4, 1.2)

    # Abbe lateral resolution
    lateral = 0.61 * wavelength / NA

    # Axial resolution
    axial = 2 * wavelength / (NA**2)

    st.success(f"Lateral Resolution ≈ {lateral:.2f} nm")
    st.success(f"Axial Resolution ≈ {axial:.2f} nm")


# =========================
# 3D PSF Viewer
# =========================
def psf_module():

    st.header("🌊 3D PSF Viewer")

    NA = st.slider("NA", 0.3, 1.4, 1.2)
    wavelength = st.slider("Wavelength (nm)", 400, 700, 520)

    # Grid
    size = 100
    x = np.linspace(-5, 5, size)
    y = np.linspace(-5, 5, size)
    z = np.linspace(-5, 5, size)

    X, Y = np.meshgrid(x, y)

    # Simplified Gaussian PSF model
    sigma_xy = wavelength / NA
    sigma_z = wavelength / (NA**2)

    psf_xy = np.exp(-(X**2 + Y**2)/(2*sigma_xy**2))

    # Show XY slice
    fig, ax = plt.subplots()
    im = ax.imshow(psf_xy, extent=[-5,5,-5,5])
    ax.set_title("PSF XY Slice")

    st.pyplot(fig)

    # Z profile
    psf_z = np.exp(-(z**2)/(2*sigma_z**2))

    fig2, ax2 = plt.subplots()
    ax2.plot(z, psf_z)
    ax2.set_title("PSF Z Profile")

    st.pyplot(fig2)


# =========================
# MAIN MENU
# =========================
st.title("🔬 Murphy Phase 2 - NA & Resolution")

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Numerical Aperture",
        "Resolution Calculator",
        "3D PSF Viewer"
    ]
)

if menu == "Numerical Aperture":
    NA_module()

elif menu == "Resolution Calculator":
    resolution_module()

elif menu == "3D PSF Viewer":
    psf_module()
