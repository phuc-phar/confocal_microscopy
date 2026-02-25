import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show():

    st.header("🌈 Light Fundamentals")

    wavelength = st.slider("Wavelength (nm)", 380, 750, 550)

    c = 3e8
    h = 6.626e-34

    frequency = c / (wavelength * 1e-9)
    energy = h * frequency

    st.write(f"Frequency: {frequency:.2e} Hz")
    st.write(f"Photon Energy: {energy:.2e} Joules")

    # Visible color preview
    def wavelength_to_rgb(wavelength):
        gamma = 0.8
        if 380 <= wavelength <= 440:
            r = -(wavelength - 440) / (440 - 380)
            g = 0
            b = 1
        elif 440 <= wavelength <= 490:
            r = 0
            g = (wavelength - 440) / (490 - 440)
            b = 1
        elif 490 <= wavelength <= 510:
            r = 0
            g = 1
            b = -(wavelength - 510) / (510 - 490)
        elif 510 <= wavelength <= 580:
            r = (wavelength - 510) / (580 - 510)
            g = 1
            b = 0
        elif 580 <= wavelength <= 645:
            r = 1
            g = -(wavelength - 645) / (645 - 580)
            b = 0
        else:
            r, g, b = 1, 0, 0
        return (r, g, b)

    color = wavelength_to_rgb(wavelength)

    st.markdown(
        f"<div style='width:200px;height:50px;background-color:rgb({int(color[0]*255)},{int(color[1]*255)},{int(color[2]*255)});'></div>",
        unsafe_allow_html=True
    )
