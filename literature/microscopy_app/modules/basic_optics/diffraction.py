import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1

def show():

    st.header("🌊 Diffraction & Airy Disk")

    wavelength = st.slider("Wavelength (nm)", 400, 700, 520)
    NA = st.slider("Numerical Aperture", 0.2, 1.4, 1.2)

    r = np.linspace(0.01, 10, 500)

    k = 2 * np.pi / wavelength
    airy = (2 * j1(r) / r)**2

    resolution = 0.61 * wavelength / NA

    st.success(f"Resolution Limit ≈ {resolution:.2f} nm")

    fig, ax = plt.subplots()
    ax.plot(r, airy)
    ax.set_title("Airy Disk Intensity")

    st.pyplot(fig)
