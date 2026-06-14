import streamlit as st
from models.mmsk_model import MMsK
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

    st.header("Modelo M/M/s>1/K")

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mmsk")

    with col2:
        mi = input_mi("mmsk")

    col3, col4 = st.columns(2)
    with col3:
        k = st.number_input(
            "Capacidade Máxima (K)",
            min_value=1,
            step=1,
            key="mmsk_k"
        )

    with col4:
        s = st.number_input(
            "Servidores (s)",
            min_value=1,
            step=1,
            key="mmsk_s"
        )

    st.subheader("Parâmetros opcionais")

    col5, col6 = st.columns(2)

    with col5:
        usar_n = st.checkbox("Usar n", key="mmsk_usar_n")

    n = None

    if usar_n:
        n = st.number_input(
            "n",
            min_value=0,
            max_value=int(k),
            step=1,
            key="mmsk_n"
        )
    st.divider()

    if st.button("Calcular", key="mmsk_btn"):

        try:
            fila = MMsK(lambda_, mi, k, s)

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

        st.subheader("Resultados condicionais")
        
        c7, c8, c9 = st.columns(3)
        
        with c7:
            pass

        if usar_n:
            prob_n = fila.prob_n(n)
            with c8:
                with st.container(border=True):
                    st.metric(
                        "Prob. de haver n clientes", 
                        f"{prob_n:.4g}",
                        help=f"{prob_n*100:.2f}%"
                        )
        
        with c9:
            pass