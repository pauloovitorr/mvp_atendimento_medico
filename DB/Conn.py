from mysql import connector
from mysql.connector import Error

class conexao:
    def _conn(self):
        
        try:
            conexao = connector.connect(
            host='148.113.211.197',
            user='comtest_medico',
            password='87nS~a*AS)pA',
            database='comtest_langchain',
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
        

