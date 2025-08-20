from DataBase.Conn import Conexao


class MensagemModel:
    def __init__(self, tipo_msg, texto, origem, dt_msg, id_con, res='n'):
        self.tipo_msg  = tipo_msg
        self.texto     = texto
        self.origem    = origem
        self.dt_msg    = dt_msg
        self.res       = res
        self.id_con    = id_con
        
    def cria_mensagem(self):
        conn, cursor = None, None
        try:
            conn, cursor = Conexao().conn()           
            
            sql = 'INSERT INTO mensagem (tipo_men, texto, origem, dt_men, respondido, conversa_id_con) VALUES (%s, %s, %s, %s, %s, %s)'
            
            dados_insert = (self.tipo_msg, self.texto, self.origem ,self.dt_msg, self.res, self.id_con)
            cursor.execute(sql, dados_insert)
            conn.commit()
            
            id_mensagem = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return {
                    "res":"Mensagem criada com sucesso!",
                    "id_mensagem": id_mensagem
                }
            
        except Exception as err:
            print('err: ' , err)
            conn.rollback()
            cursor.close()
            conn.close()
            
            return {
                "res":"Erro ao criar mensagem " ,
                "id_mensagem": ''
            }
            
    def lista_mensagem(self):
        conn, cursor = None, None
        try:
            conn, cursor = Conexao().conn()
            
            sql = 'SELECT * FROM mensagem where conversa_id_con = %s'
            dados_select = (self.id_con)
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
                "res":"Erro ao listar de mensagens" ,
                "id_mensagem": ''
            }
