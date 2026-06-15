import streamlit as st
from models.mms_model import MMS
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

    st.header("Modelo M/M/s>1")

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mms")

    with col2:
        mi = input_mi("mms")

    col3, = st.columns(1)

    with col3:
        s = st.number_input(
            "Servidores (s)",
            min_value=2,
            step=1,
            key="mms_s"
        )

    st.subheader("Parâmetros opcionais")

    col4, col5 = st.columns(2)

    with col4:
        usar_n = st.checkbox("Usar n", key="mms_usar_n")

    with col5:
        usar_t = st.checkbox("Usar t", key="mms_usar_t")

    n = None
    t = None
    tipo_n = None

    if usar_n:
        n = st.number_input(
            "n",
            min_value=0,
            step=1,
            key="mms_n"
        )

        tipo_n = st.selectbox(
            "Tipo de probabilidade",
            [
                "P(N=n)",
                "P(N≤n)",
                "P(N≥n)"
            ],
            key="mms_tipo_n"
        )

    if usar_t:
        t_str = st.number_input(
            "t",
            min_value=0.0,
            step=0.1,
            key="mms_t"
        )

        try:
            t = float(t_str) if t_str else None
        except:
            st.error("Digite um número válido para t")
            t = None

    st.divider()

    if st.button("Calcular", key="mms_btn"):

        try:
            fila = MMS(lambda_, mi, s)

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

            with c7:
                with st.container(border=True):
                    st.metric(
                        titulo,
                        f"{resultado:.4g}",
                        help=f"{resultado*100:.2f}%"
                    )

        if usar_t and t is not None:

            prob_sys = fila.prob_wait_system_greater_than(t)
            prob_q = fila.prob_wait_queue_greater_than(t)

            with c8:
                with st.container(border=True):
                    st.metric(
                        "Prob. W > t",
                        f"{prob_sys:.4g}",
                        help=f"{prob_sys*100:.2f}%"
                    )

            with c9:
                with st.container(border=True):
                    st.metric(
                        "Prob. Wq > t",
                        f"{prob_q:.4g}",
                        help=f"{prob_q*100:.2f}%"
                    )