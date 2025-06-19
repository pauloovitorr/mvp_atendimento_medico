from DB.Conn import conexao

class Menssagem:
    def __init__(self, tipo_mensagem, texto_mensagem, id_conversa):
        self._tipo_mensagem     = tipo_mensagem
        self._texto_mensagem    = texto_mensagem
        self._id_conversa       = id_conversa  
              
    def _lista_mensagens_conversa(self):
        conect = conexao()
        conn, cursor = conect._conn()
        
        if not conn or not cursor:
            print("Não foi possível conectar ao banco.")
            return
        
        try:
            
            sql_verifica_id_conversa = """
            SELECT 
                msg.id_mensagens,
                msg.tipo,
                msg.texto,
                msg.conversa_id_conversa,
                con.nome_paciente,
                con.tel_paciente,
                con.usuario_id_usuario,
                us.nome_medico,
                us.especialidade,
                us.email,
                us.telefone
            FROM mensagens AS msg
            INNER JOIN conversa AS con ON con.id_conversa = msg.conversa_id_conversa
            INNER JOIN usuario AS us ON con.usuario_id_usuario = us.id_usuario
            WHERE msg.conversa_id_conversa = %s
            """
            valores = (self._id_conversa,)


            cursor.execute(sql_verifica_id_conversa, valores)
            lista_mensagens = cursor.fetchall()        
      
            if lista_mensagens:
                
                cursor.close()
                conn.close()
                    
                return {
                    "res":"Mensagens com o médico encontrada",
                    "conversa": lista_mensagens
                    }
                           
                
            else:
                cursor.close()
                conn.close()
                
                return {
                    "res":"Não foi encontrado mensagens",
                     "conversa": ""
                }
            
                       
        except Exception as err:
            
            conn.rollback()
            cursor.close()
            conn.close()
            return {
                    "res":"Erro ao listar mensagens " + str(err),
                    "conversa": ""
                }


    def _cria_mensagem(self):
        conect = conexao()
        conn, cursor = conect._conn()
        
        if not conn or not cursor:
            print("Não foi possível conectar ao banco.")
            return
        
        try:
            
            sql_insert      = "INSERT INTO mensagens (tipo, texto, conversa_id_conversa) VALUES (%s, %s, %s)"
            dados_insert    = [self._tipo_mensagem , self._texto_mensagem, self._id_conversa]
            cursor.execute(sql_insert,dados_insert)
            conn.commit()
                
            id_mensagem = cursor.lastrowid
                
            cursor.close()
            conn.close()
                
            return {
                    "res":"Mensagem adicionada com sucesso!",
                    "id_mensagem": id_mensagem
            }
            
        except Exception as err:
            
            conn.rollback()
            cursor.close()
            conn.close()
            
            return {
                    "res":"Erro ao inserir conversa " + str(err),
                    "id_conversa": ''
                }
            
    @property
    def tipo_mensagem(self):
        return self._tipo_mensagem

    @tipo_mensagem.setter
    def tipo_mensagem(self, tipo):
        self._tipo_mensagem = tipo
        
    
    @property
    def texto_mensagem(self):
        return self._texto_mensagem

    @texto_mensagem.setter
    def texto_mensagem(self, texto):
        self._texto_mensagem = texto

    @property
    def id_conversa(self):
        return self._id_conversa

    @id_conversa.setter
    def id_conversa(self, id_conversa):
        self._id_conversa = id_conversa


# a = Menssagem('Humano', 'Estou ótimo', 1)
# msg = a._lista_mensagens_conversa()
# print(len(msg['conversa']))