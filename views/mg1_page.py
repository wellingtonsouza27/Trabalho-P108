import streamlit as st

from models.mg1_model import MG1
from utils.input_helpers import input_lambda
from utils.input_helpers import input_mi


def render():
    st.markdown("""
        <style>
        [data-testid="stMetric"] {
            text-align: center;
        }
        [data-testid="stMetricLabel"] {
            display: flex;
            justify-content: center;
        }
        [data-testid="stMetricValue"] {
            display: flex;
            justify-content: center;
        }
        </style>
        """, unsafe_allow_html=True)

    st.header("Modelo M/G/1")

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mg1")

    with col2:
        mi = input_mi("mg1")

    st.divider()

    if st.button("Calcular", key="mg1_btn"):

        try:
            fila = MG1(lambda_, mi)

        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados principais")

        c1, c2, c3 = st.columns(3)

        with c1:
            with st.container(border=True):
                st.metric("Taxa de ocupação (ρ)", f"{fila.rho:.4g}")

        with c2:
            with st.container(border=True):
                st.metric(
                    "Prob. do sistema ocioso (P0)",
                    f"{fila.p0:.4g}",
                    help=f"{fila.p0*100:.2f}%"
                )

        with c3:
            with st.container(border=True):
                st.metric("Número médio no sistema (L)", f"{fila.avg_clients_system():.4g}")

        c4, c5, c6 = st.columns(3)

        with c4:
            with st.container(border=True):
                st.metric("Número médio na fila (Lq)", f"{fila.avg_clients_queue():.4g}")

        with c5:
            with st.container(border=True):
                st.metric("Tempo médio no sistema (W)", f"{fila.avg_time_system():.4g}")

        with c6:
            with st.container(border=True):
                st.metric("Tempo médio na fila (Wq)", f"{fila.avg_time_queue():.4g}")