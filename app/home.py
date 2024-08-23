from screens.home_page import home_page
from screens.planos_page import planos_page

from streamlit_option_menu import option_menu
import streamlit as st
import os


def get_api_address():
    return f"http://{os.environ['API_ADDRESS']}:{os.environ['API_PORT']}"


# Configuração de metadados da página
st.set_page_config(
    page_title="Jiga de testes",
    layout="wide",
)

# Cria navegação entre as páginas
page = option_menu(
    None,
    ["Página inicial", "Planos"],
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
        home_page(get_api_address())
    case "Planos":
        planos_page(get_api_address())
