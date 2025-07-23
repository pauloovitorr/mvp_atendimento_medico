import os
import requests
from dotenv import load_dotenv
import base64
import uuid
from datetime import datetime
from openai import OpenAI

load_dotenv()


class WhatsappTranscriptionService:
    def __init__(self):
        self.server_url = os.getenv("server_url")
        self.instance = os.getenv("instance")
        self.apikey = os.getenv("apikey")
        self.headers = {
            "Content-Type": "application/json",
            "apikey": self.apikey
        }

    def get_base64(self, message_id: str) -> str | None:
       
        endpoint = f"{self.server_url}/chat/getBase64FromMediaMessage/{self.instance}"
        payload = {
            "message": {
                "key": {
                    "id": message_id
                },
                "convertToMp4": False
            }
        }

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()

            data = response.json()
            return data.get("base64")

        except requests.RequestException as e:
            print(f"Erro ao obter base64 do áudio: {e}")
            return None

    def salvar_base64_como_audio(self, base64_data: str, extensao="mp3") -> str:
        if not os.path.exists("Audios"):
            os.makedirs("Audios")

        # Caso o base64 venha com prefixo, remove
        if "," in base64_data:
            base64_data = base64_data.split(",")[1]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"audio_{timestamp}_{uuid.uuid4().hex[:6]}.{extensao}"
        caminho_arquivo = os.path.join("Audios", nome_arquivo)

        try:
            with open(caminho_arquivo, "wb") as f:
                f.write(base64.b64decode(base64_data))
            return caminho_arquivo
        except Exception as e:
            print(f"Erro ao salvar o arquivo de áudio: {e}")
            return None
        
    def transcricao_audio(self,file_audio:str) -> str:
        client = OpenAI(api_key= os.getenv('api_openai'))
        with open(file_audio, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
                prompt=
            "Você está transcrevendo áudios de um atendimento médico automatizado. "
            "O paciente pode falar sintomas, dúvidas sobre saúde, ou pedir orientações simples. "
            "Evite erros com termos médicos como: febre, pressão, consulta, receita, sintomas, dor de cabeça, etc."
        
            )
        
        return transcription
    
    def salvar_base64_como_imagem(self, base64_data: str, extensao="jpg") -> str:
        if not os.path.exists("Images"):
            os.makedirs("Images")

    
        if "," in base64_data:
            base64_data = base64_data.split(",")[1]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"imagem_{timestamp}_{uuid.uuid4().hex[:6]}.{extensao}"
        caminho_arquivo = os.path.join("Images", nome_arquivo)

        try:
            with open(caminho_arquivo, "wb") as f:
                f.write(base64.b64decode(base64_data))
            return caminho_arquivo
        except Exception as e:
            print(f"Erro ao salvar o arquivo de imagem: {e}")
            return None