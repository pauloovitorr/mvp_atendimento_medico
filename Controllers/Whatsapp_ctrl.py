import requests
from flask import request, jsonify
from Models.Conversa import Conversa
from Models.Mensagens import Menssagem
from Service.Service_whats import Service
from dotenv import load_dotenv
import os

load_dotenv()

class WhatsappCtrl:

    @staticmethod
    def index():
        try:
          
            dados = request.json
            service = Service(dados)
            response = service.valida_dados()

            if not response['success']:
                return jsonify({
                    "success": False,
                    "message": response['error']
                }), 400  

            data = response['data']
            num_cliente = data['num_cliente']
            num_usuario = data['num_usuario']
            msg_cliente = data['msg_cliente']
            nome_cliente = data['nome_cliente']
            from_me = data['from_me']

            conversa = Conversa(nome_cliente, num_cliente, num_usuario)
            cod_conversa = conversa._lista_dados_conversa()

            if not cod_conversa.get('id_conversa'):
                cod_conversa = conversa._cria_conversa()

            if not cod_conversa.get('id_conversa'):
                return jsonify({
                    "success": False,
                    "message": "Não foi possível criar ou localizar a conversa."
                }), 500  

            
            msgs = Menssagem("Humano", msg_cliente, cod_conversa['id_conversa'])
            res = msgs._cria_mensagem()

            if isinstance(res, dict):
                sucesso = res.get('res') == "Mensagem adicionada com sucesso!"
            else:
                sucesso = res == "Mensagem adicionada com sucesso!"

            if not sucesso:
                return jsonify({
                    "success": False,
                    "message": "Erro ao criar mensagem."
                }), 500

            lista_mensagens = msgs._lista_mensagens_conversa()

            
            headers = {
                "Content-Type": "application/json",
                "apiKey": os.getenv('api_evo')
            }

            body = {
                "number": num_cliente,
                "text": 'resposta',
                "delay": 1200
            }

            evo_response = requests.post(os.getenv('url_evo'), headers=headers, json=body)

            if evo_response.ok:
                return jsonify({
                    "success": True,
                    "message": "Mensagem enviada com sucesso.",
                    "conversa_id": cod_conversa['id_conversa'],
                    "mensagens": lista_mensagens
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "message": "Falha ao enviar resposta via EVO."
                }), 502  

        except Exception as e:
            
            return jsonify({
                "success": False,
                "message": "Erro interno no servidor."
            }), 500
