import streamlit as st
from views import mm1_page, mms_page, mm1k_page, mmsk_page

st.title("Simulador de Filas")

tab1, tab2, tab3, tab4 = st.tabs(["M/M/1", "M/M/s>1", "M/M/1/K", "M/M/s>1/K"])

with tab1:
    mm1_page.render()

with tab2:
    mms_page.render()

with tab3:
    mm1k_page.render()

with tab4:
    mmsk_page.render()