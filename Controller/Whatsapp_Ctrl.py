import requests
from flask import request
from dotenv import load_dotenv
from Service.Whatsapp_service import WhatsappService

class WhatsappCtrl:
    def __init__(self):
        self.service = WhatsappService()

    def index(self):
        body = request.json
        dados = self.service.limpa_dados(body)
        print(dados)
        return {"status": "ok"}, 200