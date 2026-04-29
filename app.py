import streamlit as st
from models_pages import mm1_page

st.title("Simulador de Filas")

tab1 = st.tabs(["M/M/1"])[0]

with tab1:
    mm1_page.render()
