import json
import requests
import streamlit as st
from flask import Flask
from loguru import logger
import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import socket
from streamlit_autorefresh import st_autorefresh


def get_local_ip():
    try:
        # Cria um socket para buscar o IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))  # Conecta a um endereço externo (neste caso, o Google DNS)
        local_ip = sock.getsockname()[0]  # Obtém o IP de rede local
        sock.close()
        return local_ip
    except Exception as e:
        st.error(f"Erro ao obter o IP local: {e}")
        return None


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

def temperature_page():

    # Realizando um auto-refresh na página a cada 10 segundos
    st_autorefresh(interval=10 * 1000)

    ip = get_local_ip()

    # Exibindo o status do sistema
    response = requests.get(f"http://{ip}:5000/api/planos")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())

    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    except:
        pass

    # Inserindo os dados de temperatura
    if df.empty or (df["timestamp"].max() <= (datetime.now() - timedelta(seconds=10))):
        response = requests.post(f"http://{ip}:5000/api/plano/temperatura")

    response = requests.get(f"http://{ip}:5000/api/planos")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
    
    # Obtendo o id do último plano com o nome "temperatura" e status "finalizado"r
    df = df[(df["nome"] == "temperatura") & (df["status"] == "finalizado")]
    df = df.sort_values("id", ascending=False).head(1)

    # Pegando o timestamp do último plano
    try:
        timestamp = df["timestamp"].values[0]
        timestamp = pd.to_datetime(timestamp)
    except:
        st.stop()

    # Exibindo o último horário de refresh da página
    st.write(f"Último refresh: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    # Obtendo o ID do último plano
    try:
        plano_id = df["id"].values[0]
    except:
        return

    # Obtendo os resultados dos testes
    response = requests.get(f"http://{ip}:5000/api/planos/{plano_id}")
    if response.status_code == 200:
        last_result = pd.DataFrame(response.json())
    
    df_dados = pd.DataFrame(response.json()['dados'])
    df_vereditos = pd.DataFrame(response.json()['vereditos'])

    # Removendo a coluna timestamp que ficará duplicada ao juntar os dataframes
    df_dados.drop(columns=['timestamp'], inplace=True)

    # Juntando os 2 dataframes pelo index das colunas, mantendo a quantidade de linhas
    last_result = pd.concat([df_dados, df_vereditos], axis=1)

    last_result["timestamp"] = pd.to_datetime(last_result["timestamp"])

    columns = st.columns(len(last_result))

    # Criando caixas coloridas indicando o status de cada sensor
    for idx, row in last_result.iterrows():
        with columns[idx]:
            color = 'green' if row['resultado'] == 'pass' else 'red'
            box_component(color, f"{row['temperatura']}º", row['sensor'])

    # Criando uma lista com todos os sensores
    sensors = last_result['sensor'].unique()

    # Realizando uma busca na API para obter os dados de temperatura por sensor
    fig = None
    colors = px.colors.qualitative.Plotly
    for i in range(len(sensors)):
        response = requests.get(f"http://{ip}:5000/api/sensores/{sensors[i]}")
        if response.status_code == 200:
            df_dados = pd.DataFrame(response.json()['dados'])
            df_vereditos = pd.DataFrame(response.json()['vereditos'])
            df_dados.drop(columns=['timestamp'], inplace=True)
            df_sensor = pd.concat([df_dados, df_vereditos], axis=1)
            df_sensor["timestamp"] = pd.to_datetime(df_sensor["timestamp"])
            df_sensor = df_sensor.sort_values("timestamp")
            df_sensor = df_sensor[df_sensor["timestamp"] >= (datetime.now() - timedelta(minutes=5))]
            if fig is None:
                fig = px.line(df_sensor, x="timestamp", y="temperatura", title=f"Temperatura dos sensores", color_discrete_sequence=[colors[i]])
            else:
                trace = px.line(df_sensor, x="timestamp", y="temperatura", title=f"Temperatura dos sensores", color_discrete_sequence=[colors[i]]).data[0]
                trace.hovertemplate = f"Sensor {sensors[i]}<br>" + trace.hovertemplate
                fig.add_trace(trace)
    
    if fig is not None:
        st.plotly_chart(fig)