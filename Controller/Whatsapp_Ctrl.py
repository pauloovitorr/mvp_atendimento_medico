import requests
from flask import request
from dotenv import load_dotenv
from Service.Whatsapp_service import WhatsappService

class WhatsappCtrl:
    @staticmethod
    def index():
        body = request.json
        # print(body)
        dados = WhatsappService._limpa_dados(body)
        print(dados)
        return {"status": "ok"}, 200
        