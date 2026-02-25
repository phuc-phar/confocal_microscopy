import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show():

    st.header("🔍 Lens Imaging Simulator")

    f = st.slider("Focal length (mm)", 10, 100, 50)
    obj_distance = st.slider("Object distance (mm)", 20, 200, 100)

    img_distance = 1 / (1/f - 1/obj_distance)
    magnification = -img_distance / obj_distance

    st.write(f"Image Distance: {img_distance:.2f} mm")
    st.write(f"Magnification: {magnification:.2f}")

    # Ray tracing visualization
    fig, ax = plt.subplots()

    # Lens line
    ax.axvline(0)

    # Object
    ax.plot([-obj_distance], [1], 'ro')

    # Image
    ax.plot([img_distance], [magnification], 'go')

    # Rays
    ax.plot([-obj_distance, 0], [1, 1])
    ax.plot([0, img_distance], [1, magnification])

    ax.set_title("Ray Tracing")
    ax.set_xlim(-200, 200)
    ax.set_ylim(-5, 5)

    st.pyplot(fig)
