import streamlit as st

def calculate_rate(times):
    if len(times) == 0 or sum(times) == 0:
        return 0
    return len(times) / sum(times)


def input_rate(symbol, key_prefix):
    
    value_str = st.text_input(
        symbol,
        placeholder=f"Ex: 3 (clientes/hora)",
        key=f"{key_prefix}_input"
    )

    try:
        return float(value_str) if value_str else 0
    except:
        st.error(f"Digite um número válido para {symbol}")
        return 0

        value = calculate_rate(times)

        st.info(f"{symbol} calculado: {value:.4f}")

        return value


def input_lambda(prefix=""):
    return input_rate("λ", f"{prefix}_lambda")

def input_mi(prefix=""):
    return input_rate("μ", f"{prefix}_mi")


def input_float(label, placeholder):
    value_str = st.text_input(label, placeholder=placeholder)

    try:
        return float(value_str) if value_str else 0
    except:
        st.error(f"Digite um número válido para {label}")
        return 0