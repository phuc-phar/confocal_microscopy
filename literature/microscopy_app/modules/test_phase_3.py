import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Murphy Phase 3 - Image Formation & Detection")


# ===================================
# IMAGE CONTRAST SIMULATION
# ===================================
def contrast_module():

    st.header("🔍 Image Contrast Simulator")

    contrast_type = st.selectbox(
        "Select Contrast Mechanism",
        ["Absorption", "Fluorescence", "Phase Contrast"]
    )

    size = 200
    x = np.linspace(-5, 5, size)
    y = np.linspace(-5, 5, size)
    X, Y = np.meshgrid(x, y)

    # Object model
    obj = np.exp(-(X**2 + Y**2))

    if contrast_type == "Absorption":
        image = 1 - obj

    elif contrast_type == "Fluorescence":
        image = obj

    elif contrast_type == "Phase Contrast":
        phase = np.sin(2*np.pi*obj)
        image = np.abs(phase)

    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.set_title(f"{contrast_type} Contrast")

    st.pyplot(fig)


# ===================================
# DETECTOR COMPARISON
# ===================================
def detector_module():

    st.header("📷 Detector Comparison")

    detector = st.selectbox(
        "Detector Type",
        ["PMT", "Camera"]
    )

    photons = st.slider("Incoming Photons", 100, 10000, 2000)

    if detector == "PMT":
        QE = 0.25
        read_noise = 2

    else:
        QE = 0.70
        read_noise = 5

    signal = photons * QE
    shot_noise = np.sqrt(signal)
    total_noise = np.sqrt(shot_noise**2 + read_noise**2)

    SNR = signal / total_noise

    st.write(f"Quantum Efficiency: {QE}")
    st.write(f"Signal: {signal:.2f}")
    st.write(f"Noise: {total_noise:.2f}")
    st.success(f"SNR ≈ {SNR:.2f}")


# ===================================
# NOISE SIMULATION
# ===================================
def noise_module():

    st.header("🌊 Noise Simulation")

    photons = st.slider("Photon Signal", 100, 5000, 1000)
    read_noise = st.slider("Read Noise", 0, 20, 5)

    size = 200

    # Shot noise (Poisson)
    signal = np.random.poisson(photons, (size, size))

    # Read noise (Gaussian)
    read = np.random.normal(0, read_noise, (size, size))

    noisy_image = signal + read

    fig, ax = plt.subplots()
    ax.imshow(noisy_image)
    ax.set_title("Noisy Detector Image")

    st.pyplot(fig)


# ===================================
# SNR VISUALIZER
# ===================================
def snr_module():

    st.header("📊 Signal-to-Noise Explorer")

    photons = st.slider("Photon Count", 100, 10000, 2000)
    QE = st.slider("Quantum Efficiency", 0.1, 0.9, 0.6)
    read_noise = st.slider("Read Noise", 0, 20, 5)

    signal = photons * QE
    shot_noise = np.sqrt(signal)
    total_noise = np.sqrt(shot_noise**2 + read_noise**2)

    SNR = signal / total_noise

    st.success(f"SNR ≈ {SNR:.2f}")

    photon_range = np.linspace(100, 10000, 200)
    snr_curve = (photon_range * QE) / np.sqrt(photon_range * QE + read_noise**2)

    fig, ax = plt.subplots()
    ax.plot(photon_range, snr_curve)
    ax.set_xlabel("Photon Count")
    ax.set_ylabel("SNR")
    ax.set_title("SNR vs Photon Count")

    st.pyplot(fig)


# ===================================
# MAIN MENU
# ===================================
st.title("🔬 Murphy Phase 3 - Image Formation & Detection")

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Image Contrast",
        "Detector Comparison",
        "Noise Simulation",
        "SNR Explorer"
    ]
)

if menu == "Image Contrast":
    contrast_module()

elif menu == "Detector Comparison":
    detector_module()

elif menu == "Noise Simulation":
    noise_module()

elif menu == "SNR Explorer":
    snr_module()
