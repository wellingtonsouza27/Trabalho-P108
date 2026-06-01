import streamlit as st

from models.mg1_model import MG1
from utils.input_helpers import input_lambda
from utils.input_helpers import input_mi


def render():

    st.header("Modelo M/G/1")

    col1, col2, col3 = st.columns(3)

    with col1:
        lambda_ = input_lambda("mg1")

    with col2:
        mi = input_mi("mg1")

    with col3:
        sigma2 = st.number_input(
            "Variância σ²",
            min_value=0.0,
            value=1.0
        )

    st.divider()

    if st.button("Calcular", key="mg1_btn"):

        try:
            fila = MG1(lambda_, mi, sigma2)

        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados")

        st.write(f"ρ = {fila.rho:.4f}")
        st.write(f"P0 = {fila.p0:.4f}")

        st.write(
            f"Lq = {fila.avg_clients_queue():.4f}"
        )

        st.write(
            f"Wq = {fila.avg_time_queue():.4f}"
        )

        st.write(
            f"L = {fila.avg_clients_system():.4f}"
        )

        st.write(
            f"W = {fila.avg_time_system():.4f}"
        )