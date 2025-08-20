from DataBase.Conn import Conexao


class ConversaModel:
    def __init__(self, tell_conversa, status, id_medico):
        self.tell_conversa  = tell_conversa
        self.status         = status
        self.id_medico      = id_medico
        
    def cria_conversa(self):
        conn, cursor = None, None
        try:
            conn, cursor = Conexao().conn()
            
            
            sql_verifica_con = 'SELECT * FROM conversa where tel_con = %s and medico_id_med = %s'
            dados_select = (self.tell_conversa, self.id_medico)
            cursor.execute(sql_verifica_con, dados_select)
            res = cursor.fetchall()
            
            if res:
                cursor.close()
                conn.close()
                return {
                    "res":"Já existe uma conversa com esse telefone e médico, utilize o método para listar." ,
                    "id_conversa": ''
                }
            
            
            sql = 'INSERT INTO conversa (tel_con, status_con, dt_criacao_con, dt_atualizacao_con, medico_id_med) values (%s,%s,NOW(),NOW(), %s)'
            
            dados_insert = (self.tell_conversa, self.status, self.id_medico)
            cursor.execute(sql, dados_insert)
            conn.commit()
            
            id_conversa = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return {
                    "res":"Conversa criada com sucesso!",
                    "id_conversa": id_conversa
                }
            
        except Exception as err:
            print('err: ' , err)
            conn.rollback()
            cursor.close()
            conn.close()
            
            return {
                "res":"Erro ao criar conversa " ,
                "id_conversa": ''
            }
            
    def lista_conversa(self):
        conn, cursor = None, None
        try:
            conn, cursor = Conexao().conn()
            
            sql = 'SELECT * FROM conversa where tel_con = %s and medico_id_med = %s'
            dados_select = (self.tell_conversa, self.id_medico)
            cursor.execute(sql, dados_select)
            res = cursor.fetchall()
            
            cursor.close()
            conn.close()
            return res
                
        except Exception as err:
            print('err: ' , err)
            cursor.close()
            conn.close()
            
            return {
                "res":"Erro ao listar conversa" ,
                "id_conversa": ''
            }
