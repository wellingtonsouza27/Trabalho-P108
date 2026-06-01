import streamlit as st
from models.priority_model import PriorityQueue


def render():

    st.header("Modelo com Prioridades")

    # ── Tipo de prioridade ──────────────────────────────────────────────────
    preemptive = st.toggle(
        "Com interrupção (preemptivo)",
        value=False,
        help="Ligado = com interrupção | Desligado = sem interrupção"
    )

    st.divider()

    # ── Parâmetros globais ──────────────────────────────────────────────────
    col_s, col_mu = st.columns(2)

    with col_s:
        s = st.number_input(
            "Número de servidores (s)",
            min_value=1,
            value=1,
            step=1,
            key="priority_s"
        )

    with col_mu:
        mu_str = st.text_input(
            "μ (taxa de serviço)",
            value="40",
            key="priority_mu"
        )
        try:
            mu = float(mu_str) if mu_str else 0.0
        except ValueError:
            st.error("Digite um número válido para μ")
            mu = 0.0

    st.divider()

    # ── Classes de prioridade ───────────────────────────────────────────────
    n_classes = st.number_input(
        "Número de classes de prioridade",
        min_value=2,
        max_value=10,
        value=2,
        step=1,
        key="priority_n_classes"
    )

    st.caption("Classe 1 = maior prioridade")

    lambdas = []
    cols = st.columns(min(int(n_classes), 5))  # no máximo 5 por linha

    for k in range(int(n_classes)):
        col = cols[k % len(cols)]
        with col:
            lam_str = st.text_input(
                f"λ{k + 1} (classe {k + 1})",
                value="10",
                key=f"priority_lambda_{k}"
            )
            try:
                lam = float(lam_str) if lam_str else 0.0
            except ValueError:
                st.error(f"λ{k + 1} inválido")
                lam = 0.0
            lambdas.append(lam)

    st.divider()

    # ── Calcular ────────────────────────────────────────────────────────────
    if st.button("Calcular", key="priority_btn"):

        try:
            fila = PriorityQueue(
                lambdas=lambdas,
                mu=mu,
                s=int(s),
                preemptive=preemptive
            )
        except Exception as e:
            st.error(str(e))
            return

        mode_label = "Com interrupção" if preemptive else "Sem interrupção"
        st.subheader(f"Resultados — {mode_label}")

        st.write(f"ρ total = {fila.rho_total:.4f}")

        st.divider()

        resultados = fila.results()

        for res in resultados:
            k = res["classe"]
            st.markdown(f"**Classe {k}** (λ{k} = {res['lambda']})")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("W",  f"{res['W']:.4f}")
            col2.metric("Wq", f"{res['Wq']:.4f}")
            col3.metric("L",  f"{res['L']:.4f}")
            col4.metric("Lq", f"{res['Lq']:.4f}")