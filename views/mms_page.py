import streamlit as st
from models.mms_model import MMS
from utils.input_helpers import input_lambda, input_mi


def render():
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
            "t (minutos)",
            placeholder="Ex: 15",
            key="mms_t"
        )

        try:
            # Converte minutos para horas
            t = (float(t_str) / 60) if t_str else None

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

        st.write(f"Taxa de ocupação (ρ): {fila.rho:.4g}")

        st.write(
            f"Probabilidade do sistema ocioso (P0): "
            f"{fila.p0:.4f} ({fila.p0*100:.2f}%)"
        )

        st.write(
            f"Número médio no sistema (L): "
            f"{fila.avg_clients_system():.4g}"
        )

        st.write(
            f"Número médio na fila (Lq): "
            f"{fila.avg_clients_queue():.4g}"
        )

        st.write(
            f"Tempo médio no sistema (W): "
            f"{fila.avg_time_system():.4g}"
        )

        st.write(
            f"Tempo médio na fila (Wq): "
            f"{fila.avg_time_queue():.4g}"
        )

        st.subheader("Resultados condicionais")

        if usar_n:
            prob_n = fila.prob_n(n)

            st.write(
                f"Probabilidade de haver n clientes: "
                f"{prob_n:.4f} ({prob_n*100:.2f}%)"
            )

        if usar_t and t is not None:

            prob_sys = fila.prob_wait_system_greater_than(t)
            prob_q = fila.prob_wait_queue_greater_than(t)

            st.write(
                f"Probabilidade W > t: "
                f"{prob_sys:.6f} ({prob_sys*100:.2f}%)"
            )

            st.write(
                f"Probabilidade Wq > t: "
                f"{prob_q:.6f} ({prob_q*100:.2f}%)"
            )