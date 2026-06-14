import streamlit as st
from models.mm1_model import MM1
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

    st.header("Modelo M/M/1")

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mm1")

    with col2:
        mi = input_mi("mm1")

    st.subheader("Parâmetros opcionais")

    col3, col4, col5 = st.columns(3)

    with col3:
        usar_n = st.checkbox("Usar n", key="mm1_usar_n")

    with col4:
        usar_t = st.checkbox("Usar t", key="mm1_usar_t")

    with col5:
        usar_r = st.checkbox("Usar r", key="mm1_usar_r")

    n = t = r = None

    if usar_n:
        n = st.number_input("n", min_value=0, step=1, key="mm1_n")

    if usar_t:
        t_str = st.number_input(
            "t",
            min_value=0.0,
            step=0.1,
            key="mm1_t"
        )
        try:
            t = float(t_str) if t_str else None
        except:
            st.error("Digite um número válido para t")
            t = None

    if usar_r:
        r = st.number_input("r", min_value=0, step=1, key="mm1_r")

    st.divider()

    if st.button("Calcular", key="mm1_btn"):

        if lambda_ <= 0 or mi <= 0:
            st.warning("Informe valores válidos para λ e μ.")
            return

        if lambda_ >= mi:
            st.error("Sistema instável (λ ≥ μ)")
            return

        fila = MM1(lambda_, mi)

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

        c7, c8 = st.columns(2)

        if usar_n:
            prob_n = fila.prob_n(n)
            with c7:
                with st.container(border=True):
                    st.metric(
                        "Prob. de haver n clientes", 
                        f"{prob_n:.4g}",
                        help=f"{prob_n*100:.2f}%"
                        )

        if usar_r:
            prob_r = fila.prob_greater_r(r)
            with c8:
                with st.container(border=True):
                    st.metric(
                        "Prob. de clientes > r",
                        f"{prob_r:.4g}",
                        help=f"{prob_r*100:.2f}%"
                    )

        c9, c10 = st.columns(2)

        if usar_t and t is not None:
            prob_sys = fila.prob_wait_system_greater_than(t)
            prob_q = fila.prob_wait_queue_greater_than(t)
            with c9:
                with st.container(border=True):
                    st.metric(
                        "Prob. W > t",
                        f"{prob_sys:.4g}",
                        help=f"{prob_sys*100:.2f}%"
                    )
            
            with c10:
                with st.container(border=True):
                    st.metric(
                        "Prob. Wq > t",
                        f"{prob_q:.4g}",
                        help=f"{prob_q*100:.2f}%"
                    )