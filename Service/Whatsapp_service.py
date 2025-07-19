import re,os
from datetime import datetime
from Service.Transcricao import WhatsappAudioService

class WhatsappService:
    
    @staticmethod
    def _limpa_dados(data):
        from_me     = data['data']['key']['fromMe']             
        if not from_me:
            
            msg_conversa = WhatsappService.__extrair_conteudo(data)           
                        
            num_medico     = data['sender']
            tell_conversa  = data['data']['key']['remoteJid']
            nome_conversa  = data['data']['pushName']
            timestamp_raw  = data['data']['messageTimestamp']
            origem         = data['data']['source']

            # Regex para extrair os números
            num_medico_match = re.search(r"(\d+)", num_medico).group(1)
            tell_conversa_match = re.search(r"(\d+)", tell_conversa).group(1)

            # Convertendo timestamp para datetime
            timestamp = datetime.fromtimestamp(int(timestamp_raw))

            return {
                'tell_conversa': tell_conversa_match ,
                'num_medico': num_medico_match,
                'mensagem': msg_conversa,
                'nome_conversa': nome_conversa,
                # 'tipo_msg': tipo_msg,
                'timestamp': timestamp,
                'origem': origem
            }
            
        else:
            return None

    @staticmethod
    def __extrair_conteudo(data):
        tipo        = data['data']['messageType']
        mensagem    = data['data']['message']
        id_mensagem = data['data']['key']['id']

        if tipo == 'conversation':
            return mensagem['conversation']

        elif tipo == 'audioMessage':
            id_mensagem = data['data']['key']['id']
            whatsapp_audio = WhatsappAudioService()
            base64_audio = whatsapp_audio.get_base64_audio(id_mensagem)
            caminho_audio_mp3 = whatsapp_audio.salvar_base64_como_audio(base64_audio)
                   
        elif tipo == 'imageMessage':
            return mensagem['imageMessage']['url']
        else:
            return None
        
        
        
        