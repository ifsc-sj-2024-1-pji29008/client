# Cliente Jiga de Testes

## Sumário

- [Cliente Jiga de Testes](#cliente-jiga-de-testes)
  - [Sumário](#sumário)
  - [Tecnologias](#tecnologias)
  - [Requisitos](#requisitos)
  - [Configuração do Ambiente de Desenvolvimento](#configuração-do-ambiente-de-desenvolvimento)
    - [Clonar o repositório](#clonar-o-repositório)
    - [Criar um ambiente virtual e instalar as dependências](#criar-um-ambiente-virtual-e-instalar-as-dependências)
    - [Iniciar a aplicação](#iniciar-a-aplicação)
  - [Estrutura do Projeto](#estrutura-do-projeto)


## Tecnologias

- Streamlit
- Pandas

## Requisitos

- Python 3.11+

## Configuração do Ambiente de Desenvolvimento

Utilizando um sistema operacional baseado em Unix (Linux ou macOS), siga as instruções abaixo para configurar o ambiente de desenvolvimento.

### Clonar o repositório

```bash
git clone https://github.com/ifsc-sj-2024-1-pji29008/client.git
```

### Criar um ambiente virtual e instalar as dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Iniciar a aplicação

**obs:** antes de iniciar o cliente certifique que o servidor flask está rodando, se já estiver, só executar o comando a seguir

```bash
streamlit run app/home.py
```

## Estrutura do Projeto

```
project_root/
├── app/
│   ├── home.py          # Arquivo principal da aplicação Streamlit
│   ├── screens/         # Diretório para os arquivos de cada tela da aplicação│
├── venv/                # Ambiente virtual Python (não incluído no controle de versão)
├── requirements.txt     # Arquivo contendo todas as dependências do projeto
├── README.md            # Arquivo README com informações sobre o projeto
|__ .gitignore           # Arquivo para ignorar arquivos e diretórios no controle de versão
```
