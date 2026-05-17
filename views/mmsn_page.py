import streamlit as st
from models.mmsn_model import MMsN
from utils.input_helpers import input_lambda, input_mi


def render():
    st.header("Modelo M/M/s>1/N")

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mmsn")

    with col2:
        mi = input_mi("mmsn")

    col3, col4 = st.columns(2)
    with col3:
        N = st.number_input(
            "Clientes (N)",
            min_value=1,
            step=1,
            key="mmsn_N"
        )
    
    with col4:
        s = st.number_input(
            "Servidores (s)",
            min_value=1,
            step=1,
            key="mmsn_s"
        )

    st.subheader("Parâmetros opcionais")

    col5, col6 = st.columns(2)

    with col5:
        usar_n = st.checkbox("Usar n", key="mmsn_usar_n")

    n = None

    if usar_n:
        n = st.number_input(
            "n",
            min_value=0,
            step=1,
            key="mmsn_n"
        )
    st.divider()

    if st.button("Calcular", key="mmsn_btn"):

        try:
            fila = MMsN(lambda_, mi, N, s)

        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados principais")

        st.write(f"Taxa de ocupação (ρ): {fila.rho:.4g}")
        st.write(
            f"Probabilidade do sistema ocioso (P0): "
            f"{fila.prob_idle():.4g} ({fila.prob_idle()*100:.2f}%)"
        )
        st.write(f"Número médio no sistema (L): {fila.avg_clients_system():.4g}")
        st.write(f"Número médio na fila (Lq): {fila.avg_clients_queue():.4g}")
        st.write(f"Tempo médio no sistema (W): {fila.avg_time_system():.4g}")
        st.write(f"Tempo médio na fila (Wq): {fila.avg_time_queue():.4g}")

        st.subheader("Resultados condicionais")

        if usar_n:
            prob_n = fila.prob_n(n)
            st.write(
                f"Probabilidade de haver n clientes: "
                f"{prob_n:.4g} ({prob_n*100:.2f}%)"
            )