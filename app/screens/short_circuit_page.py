import streamlit as st
from flask import Flask
from loguru import logger
import pandas as pd
import numpy as np
import datetime
import random

def short_circuit_page():
    st.title("Detecção de Curto")
    st.write("Aqui você pode visualizar os resultados da detecção de curto-circuito.")
    

    data = {
        'timestamp': pd.date_range(start='2021-01-01', periods=100),
        'value': np.random.rand(100)
    }

    df = pd.DataFrame(data)

    # Printando o dataframe com o tamanho da página inteira
    with st.expander("Visualizar dados", expanded=True):
        st.dataframe(df, use_container_width=True)

    # Adicione o código para visualização dos resultados de detecção de curto-circuito aqui