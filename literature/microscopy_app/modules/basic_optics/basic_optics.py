import streamlit as st
from modules.basic_optics import light_properties
from modules.basic_optics import lens_imaging
from modules.basic_optics import diffraction

def show():

    st.title("🔬 Basic Optics - Murphy Phase 1")

    topic = st.sidebar.radio(
        "Select Topic",
        [
            "Light Properties",
            "Lens Imaging",
            "Diffraction & Resolution"
        ]
    )

    if topic == "Light Properties":
        light_properties.show()

    if topic == "Lens Imaging":
        lens_imaging.show()

    if topic == "Diffraction & Resolution":
        diffraction.show()
