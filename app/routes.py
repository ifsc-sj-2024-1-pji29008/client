from .planos import seleciona_plano
from .jiga_data import planos_info

from flask import render_template, Blueprint, current_app

import threading

bp = Blueprint("main", __name__)


# Rota para a página inicial
@bp.route("/")
def index():
    return render_template("index.html", planos=planos_info)


@bp.route("/info/<plano>")
def plano_info(plano):
    info = planos_info.get(
        plano, {"nome": "Plano não reconhecido", "descricao": "Plano não reconhecido."}
    )
    return render_template("plano_info.html", plano=plano, info=info)


# Rota para a página de resultados
@bp.route("/plano/<plano>")
def plano_result(plano):
    info = planos_info.get(
        plano, {"nome": "Plano não reconhecido", "descricao": "Plano não reconhecido."}
    )
    # Simulando a execução dos testes em uma thread
    threading.Thread(
        target=seleciona_plano,
        args=(
            current_app.app_context(),
            plano,
        ),
    ).start()
    return render_template("plano_result.html", plano=plano, info=info)
