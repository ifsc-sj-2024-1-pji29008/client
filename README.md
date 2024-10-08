# Jiga de Testes
Este projeto é uma uma aplicação para a Raspberry Pi que possui planos de teste com o objetivo de testar sensores DS18b20 que coletam informações de temperatura e umidade do ambiente. Os planos de teste são compostos por um conjunto de regras que definem o comportamento esperado dos sensores em determinadas condições de teste. A aplicação possui uma API que controla o inicio dos testes e fornece os dados coletados pelos sensores e os vereditos de cada plano.

## Sumário

- [Jiga de Testes](#jiga-de-testes)
  - [Sumário](#sumário)
  - [Tecnologias](#tecnologias)
  - [Requisitos](#requisitos)
  - [Configuração do Ambiente de Desenvolvimento](#configuração-do-ambiente-de-desenvolvimento)
    - [Clonar o repositório](#clonar-o-repositório)
    - [Criar um ambiente virtual e instalar as dependências](#criar-um-ambiente-virtual-e-instalar-as-dependências)
    - [Iniciar a aplicação](#iniciar-a-aplicação)
  - [Trabalhando com versionamento](#trabalhando-com-versionamento)
    - [Criar um novo branch apartir do branch principal](#criar-um-novo-branch-apartir-do-branch-principal)
    - [Adicionar e commitar as alterações](#adicionar-e-commitar-as-alterações)
    - [Enviar as alterações para o repositório remoto](#enviar-as-alterações-para-o-repositório-remoto)
  - [Estrutura do Projeto](#estrutura-do-projeto)


## Tecnologias

- **Flask**: Um framework web leve e modular para Python.
- **SQLite**: Um sistema de gerenciamento de banco de dados relacional.
- **Jinja2**: Um mecanismo de template para Python.

## Requisitos

- Python 3.9+

## Configuração do Ambiente de Desenvolvimento

Utilizando um sistema operacional baseado em Unix (Linux ou macOS), siga as instruções abaixo para configurar o ambiente de desenvolvimento.

### Clonar o repositório

```bash
git clone https://github.com/ifsc-sj-2024-1-pji29008/client.git
```

Os comandos a seguir são para integração com o streamlit na branch front-end, para verificar em qual branch você está atualmente, use o seguinte comando:

```bash
git branch
```
O comando git branch listará todas as branches locais e marcará a branch atual com um asterisco (*).

Trocar para a Branch front-end caso necessário:

Para trocar para a branch front-end, primeiro, você deve garantir que a branch front-end exista. Se ela não existir, você precisará criá-la. Aqui está o que você deve fazer:

Verifique se a branch front-end existe:

```bash
git branch -a
```
Este comando listará todas as branches locais e remotas. Se a branch front-end estiver listada, você pode trocar para ela.

Trocar para a branch front-end:

Se a branch front-end já existir, você pode usar:

```bash
git checkout front-end
```

### Criar um ambiente virtual e instalar as dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Iniciar a aplicação

**obs:** antes de iniciar o front-end, certifique-se que o servidor flask está rodando, se já estiver, só executar o comando a seguir:

```bash
streamlit run app/home.py
```

## Trabalhando com versionamento
Quando for trabalhar em uma nova funcionalidade ou correção de bug, siga os passos abaixo para criar um novo branch e enviar as alterações para o repositório remoto.

### Criar um novo branch apartir do branch principal

```bash
git checkout main
git pull
git checkout -b nome-do-branch
```
Com isso já é possivel trabalhar na nova funcionalidade ou correção de bug sem que qualquer alteração afete o branch principal e vice-versa.

### Adicionar e commitar as alterações
Ao finalizar as alterações, adicione e commit as alterações feitas.

```bash
git add .
git commit -m "Mensagem do commit"
```

### Enviar as alterações para o repositório remoto

```bash
git push origin nome-do-branch
```
Com isso as alterações feitas no branch local serão enviadas para o repositório remoto. É comum que o repositório possua um `curador` que irá revisar as alterações e aceitar ou recusar as alterações. Ele que irá mesclar as alterações com o branch principal.


## Estrutura do Projeto

```
project_root/
│
├── app/
│   ├── __init__.py         # Cria e configura a aplicação Flask
│   ├── api.py              # Define os recursos da API (endpoints)
│   ├── routes.py           # Define as rotas da aplicação (endpoints)
│   ├── models.py           # Define os modelos de dados (usados com SQLAlchemy)
│   ├── database.py         # Inicializa e configura o banco de dados (SQLAlchemy)
│   ├── config.py           # Configurações da aplicação (variáveis de configuração)
│   ├── templates/          # Diretório para armazenar templates HTML
│   └── static/             # Diretório para arquivos estáticos (CSS, JS, imagens)
│
├── venv/                    # Ambiente virtual Python (não incluído no controle de versão)
│
├── logs/                    # Diretório para armazenar arquivos de log (não incluído no controle de versão)
│
├── config/                  # Diretório para configurações de implantação
│   ├── gunicorn_config.py   # Configurações do Gunicorn para execução do Flask
│   ├── nginx.conf           # Configurações do Nginx para servir o Flask via HTTP
│   └── supervisor.conf      # Configurações do Supervisor para gerenciar o processo do Flask
│
├── scripts/                 # Diretório para scripts utilitários
│   └── start_gunicorn.sh    # Script para iniciar o servidor Gunicorn
│
├── tests/                   # Diretório para testes da aplicação
│   ├── __init__.py
│   ├── test_app.py          # Testes unitários e de integração da aplicação Flask
│
├── requirements.txt         # Arquivo contendo todas as dependências do projeto
├── README.md                # Arquivo README com informações sobre o projeto
└── run.py                   # Script para iniciar a aplicação Flask em modo de desenvolvimento
