import streamlit as st
from models.mms_model import MMS
from utils.input_helpers import input_lambda, input_mi


def render():
    st.header("Modelo M/M/s (s > 1)")

    col1, col2, col3 = st.columns(3)

    with col1:
        lambda_ = input_lambda("mms")

    with col2:
        mi = input_mi("mms")

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

    n = t = None

    if usar_n:
        n = st.number_input(
            "n",
            min_value=0,
            step=1,
            key="mms_n"
        )

    if usar_t:
        t_str = st.text_input(
            "t",
            placeholder="Ex: 1.5",
            key="mms_t"
        )

        try:
            t = float(t_str) if t_str else None
        except:
            st.error("Digite valor válido para t")
            t = None

    st.divider()

    if st.button("Calcular", key="mms_btn"):

        try:
            fila = MMS(lambda_, mi, s)

        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados principais")

        st.write(f"ρ = {fila.rho:.4f}")
        st.write(f"P0 = {fila.p0:.4f}")
        st.write(f"Lq = {fila.avg_clients_queue():.4f}")
        st.write(f"Wq = {fila.avg_time_queue():.4f}")
        st.write(f"L = {fila.avg_clients_system():.4f}")
        st.write(f"W = {fila.avg_time_system():.4f}")

        st.subheader("Resultados condicionais")

        if usar_n:
            pn = fila.prob_n(n)
            st.write(f"P(n clientes) = {pn:.4f}")

        if usar_t and t is not None:
            pwq = fila.prob_wait_queue_greater_than(t)
            st.write(f"P(Wq > t) = {pwq:.4f}")

            pw = fila.prob_wait_system_greater_than(t)
            st.write(f"P(W > t) = {pw:.4f}")