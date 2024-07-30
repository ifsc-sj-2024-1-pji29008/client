import streamlit as st
from flask import Flask
from loguru import logger
import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

def get_color(color):
    match color:
        case "blue":
            color = "#009de9"
        case "green":
            color = "#009934"
        case "orange":
            color = "#e07602"
        case "red":
            color = "#cc0033"
    return color


def box_component(color="red", value=0, label="Label"):
    color = get_color(color)

    st.markdown(
        f"""
        <div style="width: 100%;
                    background-color: {color};
                    text-align: center;
                    color: white;
                    padding: 8px;
                    border-radius: 8px;
                    margin: 0 0 32px 0;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    ">
            <p style="margin: auto;">{label}</p>
            <p style="margin: auto; font-weight: 600; font-size: 1.75em">{value}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def generate_data():
    timestamps = [datetime.now() - timedelta(minutes=1 * i) for i in range(30)]
    sensors = ['Sensor 1', 'Sensor 2', 'Sensor 3']
    data = {
        'Timestamp': np.tile(timestamps, len(sensors)),
        'Sensor': np.repeat(sensors, len(timestamps)),
        'Temperatura': np.random.uniform(20, 30, len(timestamps) * len(sensors))
    }
    df = pd.DataFrame(data)
    df = df.sort_values(by='Timestamp')
    return df

def temperature_page():

    # Conectar ao banco de dados
    conn = sqlite3.connect('test_jig_teste.db')
    c = conn.cursor()

    # Loop que verifica se o valor "temperatura" na tabela "status_plano" é igual a "complete"
    c.execute("""SELECT * FROM status_plano WHERE plano = 'temperatura';""")
    data = c.fetchall()


    # Transformando data em um dataframe
    data = pd.DataFrame(data, columns=['id', 'plano', 'status'])

    if data['status'].values[0] != 'complete':
        st.write("O teste de temperatura ainda não foi concluído.")
        st.stop()

    c.execute("""SELECT * FROM sensor;""")
    data = c.fetchall()

    # Transformando data em um dataframe
    data = pd.DataFrame(data, columns=['id', 'temperature', 'verdict', 'serialNumber'])

    # Criando uma coluna com o ID do dispositivo
    data['device'] = data['serialNumber'].str[:13]

    # Obtendo a última leitura de temperatura de cada sensor
    last_readings = data.groupby('device').last().reset_index()

    # Criando uma coluna com o veredito do teste
    st.subheader("Resultado dos testes de temperatura")
    columns = st.columns(len(last_readings))

    # Criando caixas verdes ou vermelhas com a função box_component
    for idx, row in last_readings.iterrows():
        with columns[idx]:
            color = 'green' if row['verdict'] == 'pass' else 'red'
            box_component(color, f"{row['temperature']}º", row['serialNumber'])

    #TODO: adaptar para utilizar os dados reais quando os tivermos
    df = generate_data()
    fig = px.line(df, x='Timestamp', y='Temperatura', color='Sensor', title='Temperatura dos Sensores ao Longo do Tempo')
    fig.update_layout(xaxis_title='Timestamp', yaxis_title='Temperatura (°C)')
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Visualizar histórico de sensores com falha de temperatura"):
        st.dataframe(data[data['verdict'] == 'fail'])

    # Crie um dataframe com as colunas Timestamp, Sensor e Temperatura.

    conn.close()