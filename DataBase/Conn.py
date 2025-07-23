from mysql import connector
from mysql.connector import Error
import os
from dotenv import load_dotenv 

load_dotenv()

class Conexao:
    def conn(self):
        try:
            conexao = connector.connect(
                host = os.getenv('HOST'),
                user = os.getenv('USER'),
                password = os.getenv('PASSWORD'),
                database = os.getenv('DATABASE')
                )   
            
            if conexao.is_connected():
                conexao.autocommit = False
                curso = conexao.cursor(dictionary=True)
                return conexao, curso
            else:
                print('Não conectou no banco de dados')
                return None, None

        except Error as e:
            print('Erro na conexão: ' + e)
            return None, None



