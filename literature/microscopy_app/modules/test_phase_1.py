import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1


st.set_page_config(page_title="Murphy Phase 1 Optics")


# =============================
# Light Properties
# =============================
def wavelength_to_rgb(wavelength):

    gamma = 0.8

    if 380 <= wavelength <= 440:
        attenuation = 0.3 + 0.7*(wavelength-380)/(440-380)
        r = ((-(wavelength-440)/(440-380))*attenuation)**gamma
        g = 0.0
        b = (1.0*attenuation)**gamma

    elif 440 <= wavelength <= 490:
        r = 0.0
        g = ((wavelength-440)/(490-440))**gamma
        b = 1.0**gamma

    elif 490 <= wavelength <= 510:
        r = 0.0
        g = 1.0**gamma
        b = (-(wavelength-510)/(510-490))**gamma

    elif 510 <= wavelength <= 580:
        r = ((wavelength-510)/(580-510))**gamma
        g = 1.0**gamma
        b = 0.0

    elif 580 <= wavelength <= 645:
        r = 1.0**gamma
        g = (-(wavelength-645)/(645-580))**gamma
        b = 0.0

    elif 645 <= wavelength <= 750:
        attenuation = 0.3 + 0.7*(750-wavelength)/(750-645)
        r = (1.0*attenuation)**gamma
        g = 0.0
        b = 0.0
    else:
        r = g = b = 0

    return (int(r*255), int(g*255), int(b*255))


def light_module():

    st.header("🌈 Light Fundamentals")

    wavelength = st.slider("Wavelength (nm)", 380, 750, 550)

    c = 3e8
    h = 6.626e-34
    e = 1.602e-19

    wavelength_m = wavelength * 1e-9
    frequency = c / wavelength_m
    energy_eV = (h * frequency) / e

    st.write(f"Frequency: {frequency:.2e} Hz")
    st.write(f"Photon Energy: {energy_eV:.2f} eV")

    rgb = wavelength_to_rgb(wavelength)

    st.markdown(
        f"<div style='width:300px;height:60px;background-color:rgb{rgb};'></div>",
        unsafe_allow_html=True
    )

    wavelengths = np.linspace(380, 750, 200)
    freq = c / (wavelengths*1e-9)
    energy = (h*freq)/e

    fig, ax = plt.subplots()
    ax.plot(wavelengths, energy)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Energy (eV)")
    st.pyplot(fig)


# =============================
# Lens Imaging
# =============================
def lens_module():

    st.header("🔍 Lens Imaging Simulator")

    f = st.slider("Focal length (mm)", 10, 100, 50)
    obj_distance = st.slider("Object distance (mm)", 20, 200, 100)

    img_distance = 1 / (1/f - 1/obj_distance)
    magnification = -img_distance / obj_distance

    st.write(f"Image Distance: {img_distance:.2f} mm")
    st.write(f"Magnification: {magnification:.2f}")

    fig, ax = plt.subplots()

    ax.axvline(0)

    ax.plot([-obj_distance], [1], 'ro', label="Object")
    ax.plot([img_distance], [magnification], 'go', label="Image")

    ax.plot([-obj_distance, 0], [1, 1])
    ax.plot([0, img_distance], [1, magnification])

    ax.set_xlim(-200, 200)
    ax.set_ylim(-5, 5)
    ax.legend()

    st.pyplot(fig)


# =============================
# Diffraction & Airy Disk
# =============================
def diffraction_module():

    st.header("🌊 Diffraction & Resolution")

    wavelength = st.slider("Wavelength (nm)", 400, 700, 520)
    NA = st.slider("Numerical Aperture", 0.2, 1.4, 1.2)

    resolution = 0.61 * wavelength / NA

    st.success(f"Resolution Limit ≈ {resolution:.2f} nm")

    r = np.linspace(0.01, 10, 500)
    airy = (2 * j1(r) / r)**2

    fig, ax = plt.subplots()
    ax.plot(r, airy)
    ax.set_title("Airy Disk Intensity")
    st.pyplot(fig)


# =============================
# MAIN MENU
# =============================
st.title("🔬 Murphy Microscopy Phase 1")

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Light Fundamentals",
        "Lens Imaging",
        "Diffraction & Resolution"
    ]
)

if menu == "Light Fundamentals":
    light_module()

elif menu == "Lens Imaging":
    lens_module()

elif menu == "Diffraction & Resolution":
    diffraction_module()
