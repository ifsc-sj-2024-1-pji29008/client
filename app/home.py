import streamlit as st
from streamlit_option_menu import option_menu

from screens.short_circuit_page import short_circuit_page
from screens.pin_page import pin_page
from screens.temperature_page import temperature_page
from screens.home_page import home_page

# Configuração de metadados da página
st.set_page_config(
    page_title="Jiga de testes",
    layout="wide",
)

# Adiciona o logo da SensorWeb na sidebar
# with st.sidebar:
#     st.image("app/assets/logo.png")

# Cria navegação entre as páginas
page = option_menu(
    None,
    ["Página inicial", "Teste de Temperatura"],
    icons=["🏠", "thermometer-half"],
    default_index=0,
    orientation="horizontal",
    key="om_solar",
    styles={
        "nav-link-selected": {"background-color": "#00aaff"},
    },
)

match page:
    case "Página inicial":
        home_page()

    # case "Detecção de Curto":
    #     short_circuit_page()

    # case "Posição dos Pinos":
    #     pin_page()

    case "Teste de Temperatura":
        temperature_page()