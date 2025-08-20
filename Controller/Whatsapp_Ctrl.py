import requests
from flask import request
from dotenv import load_dotenv
from Service.Whatsapp_service import WhatsappService
from Models.Conversa import ConversaModel
from Models.Medico import MedicoModel
from Models.Mensagem import MensagemModel

class WhatsappCtrl:
    def __init__(self):
        self.service = WhatsappService()

    def index(self):
        body = request.json
        dados = self.service.limpa_dados(body)
        
        medico = MedicoModel(dados['num_medico'])
        lista_medico = medico.lista_medico()
                
        if lista_medico['id_med'] > 0:
            conversa = ConversaModel(dados['tell_conversa'], 'Primeiro Contato' ,lista_medico['id_med'])
            lista_con      = conversa.lista_conversa()
                        
            if not lista_con:
                res = conversa.cria_conversa()

                # Mensagens
                msg = MensagemModel(dados['tipo_msg'],dados['mensagem'], dados['origem'] ,dados['date_time'], res['id_conversa'])
                print(msg.cria_mensagem())
            else:
                msg = MensagemModel(dados['tipo_msg'],dados['mensagem'], dados['origem'] ,dados['date_time'], lista_con[0]['id_con'])
                print(msg.cria_mensagem())
                
    
        else:
            return 'Médico não encontrado'
            
        return {"status": "ok"}, 200
    
    