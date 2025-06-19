import re

class Service:
    def __init__(self, requisicao):
        self._requisicao = requisicao

    def valida_dados(self):
    
        try:
            dados = self._requisicao
            
            if not isinstance(dados, dict):
                return self._response(False, error="Requisição inválida.")

            if 'data' not in dados or 'sender' not in dados:
                return self._response(False, error="Campos obrigatórios ausentes.")

            if 'key' not in dados['data'] or 'message' not in dados['data']:
                return self._response(False, error="Campos 'key' ou 'message' ausentes em 'data'.")

            if 'conversation' not in dados['data']['message']:
                return self._response(False, error="Campo 'conversation' ausente em 'message'.")

            if 'remoteJid' not in dados['data']['key'] or 'fromMe' not in dados['data']['key']:
                return self._response(False, error="Campos 'remoteJid' ou 'fromMe' ausentes em 'key'.")

            # === Extração no seu modelo ===
            num_cliente_match = re.search(r"(\d+)@s\.whatsapp\.net", dados['data']['key']['remoteJid'])
            num_usuario_match = re.search(r"(\d+)@s\.whatsapp\.net", dados['sender'])

            if not num_cliente_match or not num_usuario_match:
                return self._response(False, error="Números inválidos.")

           
            num_cliente = num_cliente_match.group(1)
            num_usuario = num_usuario_match.group(1)
            msg_cliente = dados['data']['message']['conversation']
            nome_cliente = dados['data']['pushName']
            from_me = dados['data']['key']['fromMe']

            return self._response(True, data={
                "num_cliente": num_cliente,
                "num_usuario": num_usuario,
                "msg_cliente": msg_cliente,
                "nome_cliente": nome_cliente,
                "from_me": from_me
            })

        except Exception as e:

            return self._response(False, error="Erro interno na validação.")

    def _response(self, success, data=None, error=None):
        return {
            "success": success,
            "data": data if success else None,
            "error": error if not success else None
        }
