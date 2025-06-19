from mysql import connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

class conexao:
    def _conn(self):
        
        try:
            conexao = connector.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DATABASE'),
            use_pure=True
            )
        
            if conexao.is_connected():
                conexao.autocommit = False
                cursor = conexao.cursor(dictionary=True)
                return conexao,cursor            
            else:
                print('Não conectou no banco de dados')
                return None, None
            
        except Error as e:
            print('Erro na conexão: ' + e)
            return None, None
        

