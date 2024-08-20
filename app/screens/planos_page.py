import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import time


def iniciar_plano(api_address, nome):
    """Função para iniciar um novo plano com o nome fornecido"""
    response = requests.post(f"{api_address}/api/plano/{nome}")
    if response.status_code == 200:
        return response.json()  # Assumindo que a resposta é um JSON
    else:
        st.error("Erro ao iniciar o plano.")
        return None


def verificar_status_plano(api_address, plano_id):
    """Função para verificar o status de um plano pelo ID"""
    response = requests.get(f"{api_address}/api/planos/{plano_id}")
    if response.status_code == 200:
        return response.json()  # Assumindo que a resposta é um JSON
    else:
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


def planos_page(api_address):

    st.title("Gerenciamento de Planos")

    st.subheader("Iniciar um novo plano de testes")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Input para o nome do novo plano
        plano_nome = st.text_input("Plano")

    with col2:
        # Botão para iniciar o plano selecionado
        if st.button("Iniciar"):
            if plano_nome:
                st.info("Iniciando o plano...")
                # Enviar o POST para iniciar o plano
                plano_iniciado = iniciar_plano(api_address, plano_nome)
                if plano_iniciado:
                    plano_id = plano_iniciado.get("id")
                    st.success(
                        f"Plano iniciado com ID: {plano_id}. Verificando status..."
                    )

                    # Verificar o status do plano até ser finalizado
                    while True:
                        status = verificar_status_plano(api_address, plano_id)
                        if status:
                            st.success("Plano finalizado com sucesso!")
                            break
                        else:
                            st.warning("Aguarde...")
                        time.sleep(1)  # Esperar 5 segundos antes de verificar novamente
            else:
                st.error("Por favor, insira um nome para o plano.")

    st.subheader("Resultados do plano")
    # Carregar os planos existentes
    planos = requests.get(f"{api_address}/api/planos").json()

    # Criação do menu dropdown
    plano_opcoes = {f"{plano['nome']}:{plano['id']}": plano["id"] for plano in planos}
    plano_selecionado = st.selectbox("Selecione um plano", options=plano_opcoes.keys())

    # Obter o ID do plano selecionado
    plano_id = plano_opcoes.get(plano_selecionado)

    if plano_id:
        # Carregar e exibir os detalhes do plano selecionado
        plano_detalhes = requests.get(f"{api_address}/api/planos/{plano_id}").json()
        # st.json(plano_detalhes)  # Exibe os detalhes em formato JSON

        df_vereditos = pd.DataFrame(plano_detalhes["vereditos"])
        df_vereditos["timestamp"] = pd.to_datetime(df_vereditos["timestamp"])
        create_boxes(df_vereditos)

        # Criando uma lista com todos os sensores
        df_dados = pd.DataFrame(plano_detalhes["dados"])
        sensors = df_dados["sensor"].unique()

        # Realizando uma busca na API para obter os dados de temperatura por sensor
        fig = None
        colors = px.colors.qualitative.Plotly
        for i in range(len(sensors)):
            response = requests.get(f"{api_address}/api/sensores/{sensors[i]}")
            if response.status_code == 200:
                df_dados = pd.DataFrame(response.json()["dados"])
                df_dados["timestamp"] = pd.to_datetime(df_dados["timestamp"])
                df_dados = df_dados.sort_values("timestamp")
                # df_dados = df_dados[df_dados["timestamp"] >= (datetime.now() - timedelta(minutes=5))]
                if fig is None:
                    fig = px.line(
                        df_dados,
                        x="timestamp",
                        y="temperatura",
                        title=f"Temperatura dos sensores",
                        color_discrete_sequence=[colors[i]],
                    )
                else:
                    trace = px.line(
                        df_dados,
                        x="timestamp",
                        y="temperatura",
                        title=f"Temperatura dos sensores",
                        color_discrete_sequence=[colors[i]],
                    ).data[0]
                    trace.hovertemplate = (
                        f"Sensor {sensors[i]}<br>" + trace.hovertemplate
                    )
                    fig.add_trace(trace)

        if fig is not None:
            # Desabilitando a interpolação para que os dados sejam exibidos de forma mais fiel
            fig.update_traces(line_shape="linear")
            st.plotly_chart(fig)
