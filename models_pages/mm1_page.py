import streamlit as st
from models.mm1_model import MM1
from utils.input_helpers import input_lambda, input_mi

def render():
    st.header("Modelo M/M/1")

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda()

    with col2:
        mi = input_mi()

    st.subheader("Parâmetros opcionais")

    col3, col4, col5 = st.columns(3)

    with col3:
        usar_n = st.checkbox("Usar n")

    with col4:
        usar_t = st.checkbox("Usar t")

    with col5:
        usar_r = st.checkbox("Usar r")

    n = t = r = None

    if usar_n:
        n = st.number_input("n", min_value=0, step=1)

    if usar_t:
        t_str = st.text_input("t", placeholder="Ex: 1.5 (horas)")
        try:
            t = float(t_str) if t_str else None
        except:
            st.error("Digite um número válido para t")
            t = None

    if usar_r:
        r = st.number_input("r", min_value=0, step=1)

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

        st.write(f"Taxa de ocupação (ρ): {fila.rho:.4f}")
        st.write(f"Probabilidade do sistema ocioso (P0): {fila.prob_idle():.4f} ({fila.prob_idle()*100:.2f}%)")
        st.write(f"Número médio no sistema (L): {fila.avg_clients_system():.4f}")
        st.write(f"Número médio na fila (Lq): {fila.avg_clients_queue():.4f}")
        st.write(f"Tempo médio no sistema (W): {fila.avg_time_system():.4f}")
        st.write(f"Tempo médio na fila (Wq): {fila.avg_time_queue():.4f}")

        st.subheader("Resultados condicionais")

        if usar_n:
            prob_n = fila.prob_n(n)
            st.write(f"Probabilidade de haver n clientes: {prob_n:.4f} ({prob_n*100:.2f}%)")

        if usar_r:
            prob_r = fila.prob_greater_r(r)
            st.write(f"Probabilidade de clientes > r: {prob_r:.4f} ({prob_r * 100:.2f}%)")

        if usar_t and t is not None:
            prob_sys = fila.prob_wait_system_greater_than(t)
            prob_q = fila.prob_wait_queue_greater_than(t)
            st.write(f"Probabilidade W > t: {prob_sys:.4f} ({prob_sys*100:.2f}%)")
            st.write(f"Probabilidade Wq > t: {prob_q:.4f} ({prob_q*100:.2f}%)")
