from flask import Blueprint

atendimento = Blueprint('atendimento', __name__, url_prefix='/atendimentos')

@atendimento.route('/', methods = ['GET'])
def get_home():
    return 'Olá, mundo!'