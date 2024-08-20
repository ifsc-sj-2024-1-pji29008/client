import time
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import socket
import os

# from streamlit_autorefresh import st_autorefresh


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


def box_component(color="red", value="null", label="Label"):
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
                    min-width: 50px;
                    ">
            <p style="margin: auto;">{label}</p>
            <p style="margin: auto; font-weight: 600; font-size: 1.75em">{value}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def create_boxes(df_vereditos):
    max_elements_per_row = 6  # Defina o número máximo de elementos por linha
    num_boxes = 24  # Número total de caixas

    for i in range(0, num_boxes, max_elements_per_row):
        cols = st.columns(max_elements_per_row)
        for j in range(max_elements_per_row):
            posicao = i + j + 1
            if posicao > num_boxes:
                break
            with cols[j]:
                veredito = df_vereditos[df_vereditos["posicao"] == posicao]
                if not veredito.empty:
                    row = veredito.iloc[0]
                    color = "green" if row["resultado"] == "pass" else "red"
                    box_component(
                        color,
                        row["resultado"],
                        f"pos: {posicao} | sensor: {row['sensor']}",
                    )
                else:
                    box_component("gray", "N/A", f"{posicao}")


def temperature_test():
    pass


def temperature_page(api_address):

    # Definindo o número máximo de tentativas
    MAX_RETRIES = 300
    retry_count = 0

    # Realizando um auto-refresh na página a cada 10 segundos
    # st_autorefresh(interval=30 * 1000)
    response = requests.get(f"{api_address}/api/status")
    status = response.json()["status"]

    # Exibindo o status do sistema
    response = requests.get(f"{api_address}/api/planos")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())

    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    except:
        pass

    # Inserindo os dados de temperatura
    if status == "livre":
        response = requests.post(f"{api_address}/api/plano/temperatura")

    else:
        st.error("Não foi possível iniciar o teste de temperatura.")
        st.stop()

    dados_do_plano = response.json()

    # response = requests.get(f"{api_address}/api/planos")
    # if response.status_code == 200:
    #     df = pd.DataFrame(response.json())

    # # Obtendo o id do último plano com o nome "temperatura" e status "finalizado"r
    # df = df[(df["nome"] == "temperatura") & (df["status"] == "finalizado")]
    # df = df.sort_values("id", ascending=False).head(1)

    # # Pegando o timestamp do último plano
    # try:
    #     timestamp = df["timestamp"].values[0]
    timestamp = pd.to_datetime(dados_do_plano["timestamp"])
    # except:
    #     st.stop()

    # Exibindo o último horário de refresh da página
    st.write(f"Último refresh: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    # Loop de requisição com tentativas
    while retry_count < MAX_RETRIES:
        response = requests.get(f"{api_address}/api/planos/{dados_do_plano['id']}")
        if response.status_code == 200:
            break
        retry_count += 1
        time.sleep(1)

    if response.status_code != 200:
        st.error(
            "Não foi possível obter os resultados dos testes após várias tentativas."
        )
        st.stop()

    df_dados = pd.DataFrame(response.json()["dados"])
    df_vereditos = pd.DataFrame(response.json()["vereditos"])
    df_vereditos["timestamp"] = pd.to_datetime(df_vereditos["timestamp"])
    create_boxes(df_vereditos)

    # Criando uma lista com todos os sensores
    sensors = df_dados["sensor"].unique()

    # Realizando uma busca na API para obter os dados de temperatura por sensor
    fig = None
    colors = px.colors.qualitative.Plotly
    for i in range(len(sensors)):
        response = requests.get(f"{api_address}/api/sensores/{sensors[i]}")
        if response.status_code == 200:
            df_dados = pd.DataFrame(response.json()['dados'])
            df_dados["timestamp"] = pd.to_datetime(df_dados["timestamp"])
            df_dados = df_dados.sort_values("timestamp")
            # df_dados = df_dados[df_dados["timestamp"] >= (datetime.now() - timedelta(minutes=5))]
            if fig is None:
                fig = px.line(df_dados, x="timestamp", y="temperatura", title=f"Temperatura dos sensores", color_discrete_sequence=[colors[i]])
            else:
                trace = px.line(df_dados, x="timestamp", y="temperatura", title=f"Temperatura dos sensores", color_discrete_sequence=[colors[i]]).data[0]
                trace.hovertemplate = f"Sensor {sensors[i]}<br>" + trace.hovertemplate
                fig.add_trace(trace)

    if fig is not None:
        # Desabilitando a interpolação para que os dados sejam exibidos de forma mais fiel
        fig.update_traces(line_shape='linear')
        st.plotly_chart(fig)
