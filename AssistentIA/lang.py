from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Inicialização do LLM
llm = ChatOpenAI(
    api_key=os.getenv('api_openai'),
    model='gpt-4o-mini',
    temperature=0.2
)

class Assistent:
    def __init__(self, nome_medico, especialidade, msg_respondida=None, msg_nao_respondida=None):
        self.nome_medico = nome_medico
        self.especialidade = especialidade
        self.msg_respondida = msg_respondida or []
        self.msg_nao_respondida = msg_nao_respondida or []
        self.historico = []

        # Define o id da conversa se houver mensagens não respondidas
        self.id_conversa = None
        if self.msg_nao_respondida:
            self.id_conversa = self.msg_nao_respondida[0].get('conversa_id_con')

    def __historico_msg(self):
        # Mensagens já respondidas
        for msg in self.msg_respondida:
            if msg.get("autor") == "humano":
                self.historico.append(HumanMessage(content=msg.get('texto', '')))
            elif msg.get("autor") == "ia":
                self.historico.append(AIMessage(content=msg.get('texto', '')))

        # Mensagens ainda não respondidas (apenas humano)
        for msg in self.msg_nao_respondida:
            if msg.get("autor") == "humano":
                self.historico.append(HumanMessage(content=msg.get('texto', '')))

    def responde_msg(self):
        # Monta histórico
        self.__historico_msg()

        # Prompt do sistema
        conteudo = f"""
                    Você é um assistente virtual do(a) Dr(a). {self.nome_medico}, {self.especialidade}, responsável por organizar o agendamento de consultas.

                    Regras:
                    - Apresente-se sempre como assistente do Dr(a). {self.nome_medico}.
                    - Coleta de informações: nome, telefone, data/hora preferencial e motivo da consulta (2–3 frases).
                    - Não forneça diagnósticos ou receitas jamais.
                    - Seja educado, cordial e confirme sempre se o paciente quer prosseguir.
                    - Agradeça se o paciente desistir.

                    Objetivo:
                    Garantir que o paciente confirme data/hora e informe o motivo da consulta, recebendo resposta clara e simpática.
                    """
        # Cria lista de mensagens para enviar ao LLM
        messages = [SystemMessage(content=conteudo)] + self.historico

        # Chamada ao LLM
        response = llm.invoke(input=messages)

        return response.content
