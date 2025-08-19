import re,os
from datetime import datetime
from Service.Transcricao import WhatsappTranscriptionService

class WhatsappService:
    
    def limpa_dados(self,data):
        from_me     = data['data']['key']['fromMe']             
        if not from_me:
            
            msg_conversa = self.__extrair_conteudo(data)           
                        
            num_medico     = data['sender']
            tell_conversa  = data['data']['key']['remoteJid']
            
            timestamp_raw  = data['data']['messageTimestamp']
            origem         = data['data']['source']

            # Regex para extrair os números
            tell_conversa_match = re.search(r"(\d+)", tell_conversa).group(1)
            num_medico_match = re.search(r"(\d+)", num_medico).group(1)
            
            tipo_msg        = data['data']['messageType']
            # Convertendo timestamp para datetime
            timestamp = datetime.fromtimestamp(timestamp_raw)
            timestamp_convertido = timestamp.strftime('%Y-%m-%d %H:%M:%S')

            return {
                'tell_conversa': tell_conversa_match ,
                'num_medico': num_medico_match,
                'mensagem': msg_conversa,
                'tipo_msg': tipo_msg,
                'date_time': timestamp_convertido,
                'origem': origem
            }
            
        else:
            return None

    def __extrair_conteudo(self,data):
        tipo        = data['data']['messageType']
        mensagem    = data['data']['message']
        id_mensagem = data['data']['key']['id']

        if tipo == 'conversation':
            return mensagem['conversation']

        elif tipo == 'audioMessage':
            seconds = data['data']['message']['audioMessage']['seconds']
            
            if seconds < 1:
                return "Seu áudio veio com problema. Poderia repetir por gentileza?"
            elif seconds > 30:
                return (
                        "Recebi seu áudio, mas por enquanto consigo analisar apenas mensagens de até 30 segundos. "
                        "Você poderia resumir a mensagem em um áudio mais curto ou digitar o que deseja?"
                    )
            
            id_mensagem         = data['data']['key']['id']
            whatsapp_audio      = WhatsappTranscriptionService()
            base64_audio        = whatsapp_audio.get_base64(id_mensagem)
            caminho_audio_mp3   = whatsapp_audio.salvar_base64_como_audio(base64_audio)
            texto_do_audio      = whatsapp_audio.transcricao_audio(caminho_audio_mp3)

            return texto_do_audio
            
        elif tipo == 'imageMessage':
            whatsapp_img        = WhatsappTranscriptionService()
            base64_img          = whatsapp_img.get_base64(id_mensagem)
            texto_imagem        = whatsapp_img.transcricao_imagem(base64_img)
            
            return texto_imagem
        else:
            return 'Desculpe, ainda não consigo processar esse tipo de arquivo. Por favor, envie uma mensagem de texto, ou áudio.'
        
    