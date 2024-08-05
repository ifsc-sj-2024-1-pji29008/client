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

    ip = get_local_ip()

    # Exibindo o último horário de refresh da página
    st.write(f"Último refresh: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Exibindo o status do sistema
    response = requests.get(f"http://{ip}:5000/api/planos")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
    
    # Obtendo o id do último plano com o nome "temperatura" e status "finalizado"
    if not df.empty:
        df = df[(df["nome"] == "temperatura") & (df["status"] == "finalizado")]
        df = df.sort_values("id", ascending=False).head(1)
    else:
        st.stop()

    # Obtendo o ID do último plano
    plano_id = df["id"].values[0]

    # Obtendo os resultados dos testes
    response = requests.get(f"http://{ip}:5000/api/planos/{plano_id}")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())

    st.dataframe(df)
    st.write(response.json())
