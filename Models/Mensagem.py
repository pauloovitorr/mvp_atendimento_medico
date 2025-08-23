from DataBase.Conn import Conexao


class MensagemModel:
    def __init__(self, autor, tipo_msg, texto, origem, dt_msg, id_con, res='n'):
        self.autor      = autor
        self.tipo_msg   = tipo_msg
        self.texto      = texto
        self.origem     = origem
        self.dt_msg     = dt_msg
        self.res        = res
        self.id_con     = id_con
        
    def cria_mensagem(self):
        conn, cursor = None, None
        try:
            conn, cursor = Conexao().conn()           
            
            sql = 'INSERT INTO mensagem (autor, tipo_men, texto, origem, dt_men, respondido, conversa_id_con) VALUES (%s,%s, %s, %s, %s, %s, %s)'
            
            dados_insert = (self.autor,self.tipo_msg, self.texto, self.origem ,self.dt_msg, self.res, self.id_con)
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

            # Últimas respondidas 
            sql_resp = """
                SELECT * FROM mensagem
                WHERE conversa_id_con = %s
                AND respondido = 's'
                ORDER BY dt_men DESC
                LIMIT 10
            """
            cursor.execute(sql_resp, (self.id_con,))
            respondidas = cursor.fetchall() or []  # se não tiver nada, vira lista vazia

            # Não respondidas (todas)
            sql_nao_resp = """
                SELECT * FROM mensagem
                WHERE conversa_id_con = %s
                AND respondido = 'n'
                ORDER BY dt_men ASC
            """
            cursor.execute(sql_nao_resp, (self.id_con,))
            nao_respondidas = cursor.fetchall() or []  # idem aqui

            cursor.close()
            conn.close()

            return {
                "respondidas": list(reversed(respondidas)) if respondidas else [],
                "nao_respondidas": nao_respondidas
            }

        except Exception as err:
            print('err: ', err)
            if cursor:
                cursor.close()
            if conn:
                conn.close()

            return {
                "res": "Erro ao listar mensagens",
                "respondidas": [],
                "nao_respondidas": []
            }

    def atualiza_mensagem(self, ids, flag):
        conn, cursor = None, None
        try:
            conn, cursor = Conexao().conn()
            
            placeholders = ','.join(['%s'] * len(ids))
            sql = f'UPDATE mensagem SET respondido = %s WHERE id_men IN ({placeholders})'
            
            cursor.execute(sql, (flag, *ids))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return {
                "res": "Mensagens atualizadas com sucesso!",
                "ids_mensagens": ids
            }
            
        except Exception as err:
            print('err: ', err)
            if conn:
                conn.rollback()
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            
            return {
                "res": f"Erro ao atualizar mensagens: {err}",
                "ids_mensagens": ''
            }
