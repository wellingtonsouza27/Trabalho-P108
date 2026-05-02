import streamlit as st
from views import mm1_page, mms_page

st.title("Simulador de Filas")

tab1, tab2 = st.tabs(["M/M/1", "M/M/s>1"])

with tab1:
    mm1_page.render()

with tab2:
    mms_page.render()