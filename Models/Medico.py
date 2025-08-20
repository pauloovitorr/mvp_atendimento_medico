from DataBase.Conn import Conexao


class MedicoModel:
    def __init__(self, tell_conversa):
        self.tell_conversa  = tell_conversa
        
    def lista_medico(self):
        conn, cursor = None, None
        try:
            conn, cursor = Conexao().conn()
            sql = 'SELECT * from medico where telefone = %s'
            
            dados_select = (self.tell_conversa,)
            cursor.execute(sql, dados_select)
            dados_med = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            if dados_med:
                return {
                        "res":"Médico encontrado com sucesso",
                        "id_med": dados_med[0]['id_med']
                    }
            else:
                return {
                        "res":"Médico não encontrado",
                        "id_med": ''
                    }
            
        except Exception as err:
            print('Erro: ' , err)
            cursor.close()
            conn.close()
            return {
                    "res":"Erro ao listar médico",
                    "id_med": ''
                }
             
           