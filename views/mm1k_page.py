import streamlit as st
from models.mm1k_model import MM1K
from utils.input_helpers import input_lambda, input_mi


def render():
    st.header("Modelo M/M/1/K")

    col1, col2, col3 = st.columns(3)

    with col1:
        lambda_ = input_lambda("mm1k")

    with col2:
        mi = input_mi("mm1k")

    with col3:
        k = st.number_input(
            "Capacidade Máxima (K)",
            min_value=1,
            step=1,
            key="mm1k_k"
        )

    st.subheader("Parâmetros opcionais")

    col4, col5 = st.columns(2)

    with col4:
        usar_n = st.checkbox("Usar n", key="mm1k_usar_n")

    n = None

    if usar_n:
        n = st.number_input(
            "n",
            min_value=0,
            step=1,
            key="mm1k_n"
        )
    st.divider()

    if st.button("Calcular", key="mm1k_btn"):

        try:
            fila = MM1K(lambda_, mi, k)

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