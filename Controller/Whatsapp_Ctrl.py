import requests
from flask import request
from dotenv import load_dotenv
from Service.Whatsapp_service import WhatsappService
from Models.Conversa import ConversaModel
from Models.Medico import MedicoModel

class WhatsappCtrl:
    def __init__(self):
        self.service = WhatsappService()

    def index(self):
        body = request.json
        dados = self.service.limpa_dados(body)
        # print(dados)
        
        medico = MedicoModel('5518997607919')
        lista_medico = medico.lista_medico()
        
        if lista_medico['id_med'] > 0:
            conversa = ConversaModel(dados['tell_conversa'], 'Primeiro Contato' ,lista_medico['id_med'])

            res = conversa.cria_conversa()
            
        return {"status": "ok"}, 200
    
    