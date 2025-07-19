from flask import Blueprint
from Controller.Whatsapp_Ctrl import WhatsappCtrl

atendimento = Blueprint('atendimento', __name__, url_prefix='/atendimentos')

@atendimento.route('/', methods = ['POST'])
def post_msg():
    return WhatsappCtrl.index()