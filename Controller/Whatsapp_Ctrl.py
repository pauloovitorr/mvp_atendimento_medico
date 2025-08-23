import requests, time
from flask import request
from dotenv import load_dotenv
from Service.Whatsapp_service import WhatsappService
from Models.Conversa import ConversaModel
from Models.Medico import MedicoModel
from Models.Mensagem import MensagemModel

from AssistentIA.lang import Assistent

class WhatsappCtrl:
    def __init__(self):
        self.service = WhatsappService()

    def index(self):
        body = request.json
        dados = self.service.limpa_dados(body)
        
        # Recupera dados do médico
        medico_model = MedicoModel(dados['num_medico'])
        lista_medico = medico_model.lista_medico()
                
        if lista_medico['res'] != 'Médico encontrado com sucesso':
            return 'Médico não encontrado', 404

        # Cria ou recupera conversa
        conversa_model = ConversaModel(dados['tell_conversa'], 'Primeiro Contato', lista_medico['dados_med']['id_med'] )
        lista_conversa = conversa_model.lista_conversa()
        
        if not lista_conversa:
            # Cria nova conversa
            res_conversa = conversa_model.cria_conversa()
            id_conversa = res_conversa['id_conversa']
        else:
            # Usa a conversa existente
            id_conversa = lista_conversa[0]['id_con']

        # Cria mensagem do usuário
        msg_model = MensagemModel(
            'humano',
            dados['tipo_msg'],
            dados['mensagem'],
            dados['origem'],
            dados['date_time'],
            id_conversa
        )
        
        msg_model.cria_mensagem()
        
        time.sleep(30)
             
        lista_msgs = msg_model.lista_mensagem()
        
        print(lista_msgs)
        
        print('\n\n ****************************************************************************************** \n\n')

        # Instancia assistente com mensagens
        ia = Assistent(
            lista_medico['dados_med']['nome_med'],
            lista_medico['dados_med']['especialidade'],
            lista_msgs['respondidas'],
            lista_msgs['nao_respondidas']
        )
        
        print(ia.responde_msg())

        return {"status": "ok"}, 200
