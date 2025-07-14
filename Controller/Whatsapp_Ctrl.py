import requests
from flask import request
from dotenv import load_dotenv

class WhatsappCtrl:
    @staticmethod
    def index():
        dados = request.json
        
        