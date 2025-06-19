from DB.Conn import conexao

class Conversa:
    def __init__(self, nome_paciente, tel_paciente, tel_usuario):
        self._nome_paciente     = nome_paciente
        self._tel_paciente      = tel_paciente
        self._tel_usuario       = tel_usuario   
    
    def _lista_dados_conversa(self):
        conect = conexao()
        conn, cursor = conect._conn()
        
        if not conn or not cursor:
            print("Não foi possível conectar ao banco.")
            return
        
        try:
            
            sql_verifica_user_paciente = "SELECT id_usuario FROM usuario WHERE telefone = %s"
            telefone = (self._tel_usuario,) 
            cursor.execute(sql_verifica_user_paciente, telefone)
            id_usuario = cursor.fetchall()

            
            if id_usuario:
                sql_lista_conversa = """
                SELECT id_conversa 
                FROM conversa 
                WHERE tel_paciente = %s AND usuario_id_usuario = %s
                """
                valores = (self._tel_paciente, id_usuario[0]['id_usuario'])
                cursor.execute(sql_lista_conversa, valores)
                id_conversa = cursor.fetchall()

                
                if id_conversa:
                    conn.rollback()
                    cursor.close()
                    conn.close()
                    
                    return {
                        "res":"Convesa com o médico encontrada",
                        "id_conversa": id_conversa[0]['id_conversa']
                    }
                    
                else:
                    
                    conn.rollback()
                    cursor.close()
                    conn.close()
                    
                    return {
                        "res":"Não existe conversa com esse médico",
                        "id_conversa": ''
                    }
                                
                
            else:
                
                conn.rollback()
                cursor.close()
                conn.close()
                
                return {
                    "res":"Usuário não encontrado",
                    "id_conversa": ''
                }
            
                       
        except Exception as err:
            
            conn.rollback()
            cursor.close()
            conn.close()
            return {
                    "res":"Erro ao listar conversa " + str(err),
                    "id_conversa": ''
                }


    def _cria_conversa(self):
        conect = conexao()
        conn, cursor = conect._conn()
        
        if not conn or not cursor:
            print("Não foi possível conectar ao banco.")
            return
        
        try:

            sql_verifica_user = "SELECT id_usuario FROM usuario WHERE telefone = %s"
            valores = (self._tel_usuario,)
            
            cursor.execute(sql_verifica_user, valores)
            id_usuario = cursor.fetchall()
            
            if id_usuario:
                sql_insert = """
                    INSERT INTO conversa (nome_paciente, tel_paciente, usuario_id_usuario)
                    VALUES (%s, %s, %s)
                """
                dados_insert = (self._nome_paciente, self._tel_paciente, id_usuario[0]['id_usuario'])
                cursor.execute(sql_insert, dados_insert)

                conn.commit()
                
                id_conversa = cursor.lastrowid
                
                cursor.close()
                conn.close()
                
                return {
                    "res":"Conversa criada com sucesso!",
                    "id_conversa": id_conversa
                }
            
            else:
                
                conn.rollback()
                cursor.close()
                conn.close()
                
                return {
                    "res":"Usuário não encontrado",
                    "id_conversa": ''
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
    def nome_paciente(self):
        return self._nome_paciente

    @nome_paciente.setter
    def nome_paciente(self, nome):
        self._nome_paciente = nome
        
    
    @property
    def tel_paciente(self):
        return self._tel_paciente

    @tel_paciente.setter
    def tel_paciente(self, telefone):
        self._tel_paciente = telefone

    @property
    def tel_usuario(self):
        return self._tel_usuario

    @tel_usuario.setter
    def tel_usuario(self, telefone):
        self._tel_usuario = telefone



# a = Conversa('PP','18998989790', '18997607919' )
# print(a._cria_conversa())
