import streamlit as st
from modules import optics, resolution, fluorescence, confocal, fret

st.set_page_config(page_title="Murphy Microscopy Learning App")

st.title("🔬 Microscopy Learning - Murphy Based")

menu = st.sidebar.selectbox(
    "Choose Topic",
    [
        "Optical Basics",
        "Resolution",
        "Fluorescence Microscopy",
        "Confocal Microscopy",
        "FRET"
    ]
)

if menu == "Optical Basics":
    optics.show()

elif menu == "Resolution":
    resolution.show()

elif menu == "Fluorescence Microscopy":
    fluorescence.show()

elif menu == "Confocal Microscopy":
    confocal.show()

elif menu == "FRET":
    fret.show()
