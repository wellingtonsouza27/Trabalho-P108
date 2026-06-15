import streamlit as st
from models.mm1n_model import MM1N
from utils.input_helpers import input_lambda, input_mi


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

    st.header("Modelo M/M/1/N")

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mm1n")

    with col2:
        mi = input_mi("mm1n")

    col3, = st.columns(1)

    with col3:
        N = st.number_input(
            "Clientes (N)",
            min_value=1,
            step=1,
            key="mm1n_N"
        )

    st.subheader("Parâmetros opcionais")

    col4, col5 = st.columns(2)

    with col4:
        usar_n = st.checkbox("Usar n", key="mm1n_usar_n")

    n = None
    tipo_n = None

    if usar_n:
        n = st.number_input(
            "n",
            min_value=0,
            step=1,
            key="mm1n_n"
        )

        tipo_n = st.selectbox(
            "Tipo de probabilidade",
            [
                "P(N=n)",
                "P(N≤n)",
                "P(N≥n)"
            ],
            key="mm1n_tipo_n"
        )

    st.divider()

    if st.button("Calcular", key="mm1n_btn"):

        try:
            fila = MM1N(lambda_, mi, N)

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
                    f"{fila.prob_idle():.4g}",
                    help=f"{fila.prob_idle()*100:.2f}%"
                )

        with c3:
            with st.container(border=True):
                st.metric(
                    "Número médio no sistema (L)",
                    f"{fila.avg_clients_system():.4g}"
                )

        c4, c5, c6 = st.columns(3)

        with c4:
            with st.container(border=True):
                st.metric(
                    "Número médio na fila (Lq)",
                    f"{fila.avg_clients_queue():.4g}"
                )

        with c5:
            with st.container(border=True):
                st.metric(
                    "Tempo médio no sistema (W)",
                    f"{fila.avg_time_system():.4g}"
                )

        with c6:
            with st.container(border=True):
                st.metric(
                    "Tempo médio na fila (Wq)",
                    f"{fila.avg_time_queue():.4g}"
                )

        st.subheader("Resultados condicionais")

        c7, c8, c9 = st.columns(3)

        if usar_n:

            if tipo_n == "P(N=n)":
                resultado = fila.prob_n(n)
                titulo = "Prob. de haver exatamente n clientes"

            elif tipo_n == "P(N≤n)":
                resultado = fila.prob_less_equal_n(n)
                titulo = "Prob. de haver até n clientes"

            else:
                resultado = fila.prob_greater_equal_n(n)
                titulo = "Prob. de haver pelo menos n clientes"

            with c8:
                with st.container(border=True):
                    st.metric(
                        titulo,
                        f"{resultado:.4g}",
                        help=f"{resultado*100:.2f}%"
                    )