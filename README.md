# Simulador de Filas

Aplicação web desenvolvida em Python com Streamlit para cálculo de métricas de modelos clássicos da Teoria das Filas.

## Objetivo

O projeto foi desenvolvido para a disciplina **P108** com o objetivo de auxiliar no cálculo e análise de métricas relacionadas à Teoria das Filas, permitindo simular diferentes modelos e visualizar seus resultados de forma simples e interativa.

## Acesse o Projeto

Deploy da aplicação:

https://trabalho-p108.streamlit.app/

## Modelos Implementados

- M/M/1
- M/M/s>1
- M/M/1/K
- M/M/s>1/K

## Funcionalidades

A aplicação permite calcular métricas como:

- Taxa de ocupação (ρ)
- Probabilidade do sistema ocioso (P0)
- Número médio de clientes no sistema (L)
- Número médio de clientes na fila (Lq)
- Tempo médio no sistema (W)
- Tempo médio na fila (Wq)
- Probabilidade de haver `n` clientes no sistema
- Probabilidade de haver mais de `r` clientes
- Probabilidade de espera maior que um tempo `t`

Além disso:

- Resultados exibidos utilizando algarismos significativos;
- Validação de entradas inválidas;
- Interface organizada em abas;
- Suporte a múltiplos modelos de filas.

## Tecnologias Utilizadas

- Python
- Streamlit
- Git
- GitHub

## Como Executar o Projeto

Clone o repositório:

```bash
git clone https://github.com/wellingtonsouza27/Trabalho-P108.git
```

Acesse a pasta do projeto:

```bash
cd Trabalho-P108
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
py -m streamlit run app.py
```

## Estrutura do Projeto

```text
.
├── app.py
├── models/
├── views/
├── utils/
└── requirements.txt
```

## Interface

A aplicação possui interface web organizada por abas para facilitar a navegação entre os modelos.

## Integrantes

- Wellington Henrique Dias de Souza
- Otavio da Silva Barbosa

## Observações

Projeto desenvolvido para fins acadêmicos na disciplina P108.