import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

st.set_page_config(page_title="Confocal Education App", layout="wide")

st.title("🔬 Confocal Microscope Interactive Learning")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Choose Module",
    [
        "Introduction",
        "NA & Resolution",
        "PSF Simulation",
        "Z-stack Simulation",
        "Widefield vs Confocal",
        "Quiz"
    ]
)

# ---------------------------------------------------
# INTRODUCTION
# ---------------------------------------------------
if page == "Introduction":

    st.header("Confocal Microscopy Overview")

    st.write("""
Confocal microscopy improves image resolution and contrast by using a spatial pinhole 
to remove out-of-focus light.

Key advantages:
- Optical sectioning
- 3D imaging capability
- Improved contrast
""")

# ---------------------------------------------------
# NA & RESOLUTION
# ---------------------------------------------------
elif page == "NA & Resolution":

    st.header("Numerical Aperture & Resolution")

    NA = st.slider("Numerical Aperture (NA)", 0.3, 1.4, 0.8)
    wavelength = st.slider("Wavelength (nm)", 400, 700, 520)
    n = st.slider("Refractive Index", 1.0, 1.52, 1.33)

    # Resolution formulas
    res_xy = 0.61 * wavelength / NA
    res_z = 2 * wavelength * n / (NA ** 2)

    st.subheader("Resolution Estimates")
    st.write(f"XY Resolution ≈ {res_xy:.1f} nm")
    st.write(f"Z Resolution ≈ {res_z:.1f} nm")

    # Visual PSF width
    x = np.linspace(-3, 3, 300)
    y = np.linspace(-3, 3, 300)
    X, Y = np.meshgrid(x, y)

    sigma = 1 / NA
    psf = np.exp(-(X**2 + Y**2) / (2 * sigma**2))

    fig, ax = plt.subplots()
    ax.imshow(psf)
    ax.set_title("PSF Approximation")
    st.pyplot(fig)

# ---------------------------------------------------
# PSF SIMULATION
# ---------------------------------------------------
elif page == "PSF Simulation":

    st.header("Point Spread Function Simulation")

    NA = st.slider("NA", 0.3, 1.4, 0.8)

    x = np.linspace(-3, 3, 400)
    y = np.linspace(-3, 3, 400)
    X, Y = np.meshgrid(x, y)

    sigma = 1 / NA
    psf = np.exp(-(X**2 + Y**2) / (2 * sigma**2))

    fig, ax = plt.subplots()
    ax.imshow(psf)
    ax.set_title("PSF (Higher NA = Sharper Focus)")
    st.pyplot(fig)

# ---------------------------------------------------
# Z STACK SIMULATION
# ---------------------------------------------------
elif page == "Z-stack Simulation":

    st.header("Z-stack Sampling")

    step = st.slider("Z Step Size (µm)", 0.1, 2.0, 0.5)

    z = np.arange(-5, 5, step)
    signal = np.exp(-(z**2)/2)

    fig, ax = plt.subplots()
    ax.plot(z, signal, marker='o')
    ax.set_xlabel("Z Position")
    ax.set_ylabel("Signal Intensity")
    ax.set_title("Z-stack Sampling")

    st.pyplot(fig)

    st.write("""
Smaller step size improves sampling quality but increases acquisition time.
""")

# ---------------------------------------------------
# WIDEFIELD VS CONFOCAL
# ---------------------------------------------------
elif page == "Widefield vs Confocal":

    st.header("Widefield vs Confocal Imaging")

    noise_level = st.slider("Background Noise", 0.0, 1.0, 0.3)

    size = 256
    img = np.zeros((size, size))

    cx, cy = size // 2, size // 2
    for x in range(size):
        for y in range(size):
            if (x - cx)**2 + (y - cy)**2 < 2000:
                img[x, y] = 1

    noise = np.random.rand(size, size) * noise_level
    widefield = img + noise
    confocal = img + noise * 0.3

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Widefield")
        st.image(widefield, clamp=True)

    with col2:
        st.subheader("Confocal")
        st.image(confocal, clamp=True)

# ---------------------------------------------------
# QUIZ
# ---------------------------------------------------
elif page == "Quiz":

    st.header("Confocal Knowledge Quiz")

    score = 0

    q1 = st.radio(
        "1. What does the pinhole do?",
        [
            "Increase magnification",
            "Remove out-of-focus light",
            "Generate laser"
        ]
    )

    if q1 == "Remove out-of-focus light":
        score += 1

    q2 = st.radio(
        "2. Increasing NA will:",
        [
            "Decrease resolution",
            "Improve resolution",
            "Not affect resolution"
        ]
    )

    if q2 == "Improve resolution":
        score += 1

    q3 = st.radio(
        "3. Smaller Z step size leads to:",
        [
            "Better sampling",
            "Lower image quality",
            "No change"
        ]
    )

    if q3 == "Better sampling":
        score += 1

    if st.button("Submit"):
        st.success(f"Your Score: {score}/3")
