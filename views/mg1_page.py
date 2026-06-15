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
        sigma = st.number_input(
            "Desvio padrão do serviço (σ)",
            min_value=0.0,
            value=1.0,
            step=0.1,
            key="mg1_sigma"
        )

    st.divider()

    if st.button("Calcular", key="mg1_btn"):

        try:
            fila = MG1(lambda_, mi, sigma)

        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Taxa de ocupação (ρ)", f"{fila.rho:.4f}")

        with c2:
            st.metric("Lq", f"{fila.avg_clients_queue():.4f}")

        with c3:
            st.metric("L", f"{fila.avg_clients_system():.4f}")

        c4, c5 = st.columns(2)

        with c4:
            st.metric("Wq", f"{fila.avg_time_queue():.4f}")

        with c5:
            st.metric("W", f"{fila.avg_time_system():.4f}")