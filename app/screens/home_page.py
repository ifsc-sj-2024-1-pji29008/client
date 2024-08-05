from flask import request
import requests
import streamlit as st
import socket
import pandas as pd
from streamlit_autorefresh import st_autorefresh

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


def home_page():

    ip = get_local_ip()

    # Realizando um auto-refresh na página a cada 1 minuto
    st_autorefresh(interval=30 * 1000)

    # Exibindo o último horário de refresh da página
    st.write(f"Último refresh: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Exibindo o status do sistema
    response = requests.get(f"http://{ip}:5000/api/status")
    if response.status_code == 200:
        status = response.json()["status"]
        box_component(color="green", value=status, label="Status do sistema")
    else:
        box_component(color="red", value=response.json(), label="Status do sistema")

    # Criando 3 colunas para a página inicial
    col1, col2 = st.columns(2)

    # Listagem dos sensores
    with col1:
        with st.expander("Lista de sensores"):
            response = requests.get(f"http://{ip}:5000/api/sensores")

            # Verifica se a resposta foi bem sucedida
            if response.status_code == 200:
                # Convertendo a resposta para de json para dataframe
                df = pd.DataFrame(response.json())
                st.dataframe(df, use_container_width=True)
            else:
                st.write(response.json())

    # Botão para resetar o banco de dados
    with col2:
        if st.button("Resetar banco de dados", use_container_width=True):
            response = requests.post(f"http://{ip}:5000/api/reset")
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(response.json())