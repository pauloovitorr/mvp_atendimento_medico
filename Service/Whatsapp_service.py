import re
from datetime import datetime

class WhatsappService:
    @staticmethod
    def _limpa_dados(data):
        from_me = data['data']['key']['fromMe']

        if not from_me:
            num_medico     = data['sender']
            tell_conversa  = data['data']['key']['remoteJid']
            msg_conversa   = data['data']['message']['conversation']
            nome_conversa  = data['data']['pushName']
            tipo_msg       = data['data']['messageType']
            timestamp_raw  = data['data']['messageTimestamp']
            origem         = data['data']['source']

            # Regex para extrair os números
            tell_conversa_match = re.search(r"(\d+)", tell_conversa).group(1)
            num_medico_match = re.search(r"(\d+)", num_medico).group(1)
            

            # Convertendo timestamp para datetime
            timestamp = datetime.fromtimestamp(int(timestamp_raw))

            return {
                'tell_conversa': tell_conversa_match ,
                'num_medico': num_medico_match,
                'mensagem': msg_conversa,
                'nome_conversa': nome_conversa,
                'tipo_msg': tipo_msg,
                'timestamp': timestamp,
                'origem': origem
            }
        else:
            return None



