import streamlit as st
from models.mm1n_model import MM1N
from utils.input_helpers import input_lambda, input_mi


def render():
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

    if usar_n:
        n = st.number_input(
            "n",
            min_value=0,
            max_value=int(k),
            step=1,
            key="mm1n_n"
        )
    st.divider()

    if st.button("Calcular", key="mm1n_btn"):

        try:
            fila = MM1N(lambda_, mi, N)

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