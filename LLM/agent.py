from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv('api_openai'), temperature=0.3)


@tool
def verifica_disponibilidade_atendimento() -> dict:
    """
    Retorna uma lista de datas e horários disponíveis para consulta.
    Use esta ferramenta quando o usuário quiser saber quando pode agendar uma consulta.
    """
    return {
        "disponivel": [
            {"dia": "20/06/2025", "horarios": ["08:00", "10:00", "14:00", "18:00"]},
            {"dia": "21/06/2025", "horarios": ["07:00", "11:00", "13:00", "17:00"]}
        ]
    }
    
    

@tool
def triagem_para_atendimento(msgs: str) -> str:
    """
    Use esta ferramenta para realizar uma triagem com o paciente
    quando ele marcar data e hora.
    Pergunte o motivo da consulta, sintomas, e depois agradeça de forma cordial.
    """
    return (
        "Olá! Poderia me informar de forma breve o motivo da consulta e os sintomas principais? "
        "Assim podemos deixar tudo pronto para o atendimento."
    )
    
    
ferramentas = [verifica_disponibilidade_atendimento, triagem_para_atendimento]

    
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "Você é um assistente virtual que atua como SECRETÁRIO(A) de um consultório médico. "
            "Seu trabalho é responder educadamente, coletar informações do paciente, "
            "verificar a disponibilidade de datas e horários usando suas ferramentas, "
            "agendar consultas quando solicitado e realizar uma breve triagem perguntando o motivo da consulta e os sintomas. "
            "Use suas ferramentas sempre que for necessário para confirmar horários ou fazer a triagem. "
            "Seja cordial, objetivo e mantenha um tom profissional."
        )
    ),
    ("user", "{pergunta}"),
    ("placeholder", "{agent_scratchpad}")
])



agent = create_openai_functions_agent(llm=llm, tools=ferramentas, prompt=prompt)
agent_executor = AgentExecutor(agent= agent, tools=ferramentas)

if __name__ == '__main__':
    res = agent_executor.invoke({"pergunta": "Quero marcar uma consulta dia 19"})
    print(res['output'])