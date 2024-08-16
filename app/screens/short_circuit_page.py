import streamlit as st
from loguru import logger
import pandas as pd
import numpy as np
import datetime
import random
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

def short_circuit_page():

    ip = get_local_ip()

    # Obtendo os dados de planos