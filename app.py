import streamlit as st
import pandas as pd
from datetime import datetime

# Título do app
st.title("Calculadora de Emissões Portuárias")

# Explicação inicial
st.write("Preencha os campos abaixo para calcular os resultados de emissões portuárias automaticamente.")

# Entradas do usuário
st.header("Entradas")
codigo_entrada = st.text_input("Código de Entrada")
dtw = st.number_input("DTW (Deadweight Tonnage)", min_value=0.0, step=0.1)
categoria = st.selectbox("Categoria", ["Granel Líquido", "Granel Sólido", "Carga Geral", "Container"])
data_atracacao = st.text_input("Data de Atracação (dd/mm/yyyy HH:MM)")
data_desatracacao = st.text_input("Data de Desatracação (dd/mm/yyyy HH:MM)")

# Cálculo do P. Motor Auxiliar (kW)
if categoria:
    if categoria == "Granel Líquido":
        p_motor_aux = 200  # Valor fictício para categoria
    elif categoria == "Granel Sólido":
        p_motor_aux = 150  # Valor fictício para categoria
    elif categoria == "Carga Geral":
        p_motor_aux = 100  # Valor fictício para categoria
    elif categoria == "Container":
        p_motor_aux = 250  # Valor fictício para categoria
else:
    p_motor_aux = 0

# Validação de datas e cálculos
if codigo_entrada and dtw > 0 and categoria and data_atracacao and data_desatracacao:
    try:
        # Conversão de strings para datetime
        atracacao = datetime.strptime(data_atracacao, "%d/%m/%Y %H:%M")
        desatracacao = datetime.strptime(data_desatracacao, "%d/%m/%Y %H:%M")
        
        # Cálculos
        tempo_atracacao = desatracacao - atracacao  # Tempo total atracado
        horas_atracacao = tempo_atracacao.total_seconds() / 3600  # Conversão para horas
        energia_consumida = horas_atracacao * p_motor_aux  # Energia consumida com base no motor auxiliar
        mgo_g = dtw * horas_atracacao * 10  # Consumo de MGO em gramas (valor fictício)
        mgo_t = mgo_g / 1_000_000  # Conversão para toneladas
        co2_g = mgo_g * 3.2  # Emissão de CO2 em gramas (valor fictício)
        co2_t = co2_g / 1_000_000  # Conversão para toneladas

        # Resultados
        st.header("Resultados")
        st.write(f"**Código de Entrada:** {codigo_entrada}")
        st.write(f"**DTW (Deadweight Tonnage):** {dtw}")
        st.write(f"**Categoria:** {categoria}")
        st.write(f"**P. Motor Auxiliar (kW):** {p_motor_aux}")
        st.write(f"**Tempo de Atracação:** {tempo_atracacao}")
        st.write(f"**Horas de Atracação:** {horas_atracacao:.2f}")
        st.write(f"**Energia Consumida (kWh):** {energia_consumida:.2f}")
        st.write(f"**MGO Consumido (t):** {mgo_t:.2f}")
        st.write(f"**CO2 Liberado (t):** {co2_t:.2f}")
    
    except ValueError:
        st.error("Por favor, insira as datas no formato correto: dd/mm/yyyy HH:MM.")
else:
    st.write("Preencha todas as informações para calcular os resultados.")
