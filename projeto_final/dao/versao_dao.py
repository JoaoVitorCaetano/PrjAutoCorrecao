import mysql.connector
# Importa o ModeloDAO para permitir o lazy loading


class Versao:
   def __init__(self, idt_versao=None, nme_versao='', cod_modelo=None, vlr_modelo=None, img_modelo=''):
       self.idt_versao = idt_versao
       self.nme_versao = nme_versao
       self.cod_modelo = cod_modelo
       self.vlr_modelo = vlr_modelo
       self.img_modelo = img_modelo
       self._modelo = None  # Atributo interno para lazy loading do Modelo


   @property
   def modelo(self):
       """
       Carrega o objeto Modelo associado a esta Versao por demanda.
       """
       if self._modelo is None:
           # Cria uma instância do DAO para carregar o modelo
           from projeto_final.dao.modelo_dao import ModeloDAO
           dao = ModeloDAO()
           self._modelo = dao.selecionar_por_idt(self.cod_modelo)
       return self._modelo


   def __str__(self):
       """
       Retorna uma representação amigável do objeto.
       """
       return (f"Id: {self.idt_versao}, Nome: {self.nme_versao}, "
               f"Valor: {self.vlr_modelo}, Imagem: {self.img_modelo}, "
               f"ID do Modelo: {self.cod_modelo}, Modelo: {self.modelo.nme_modelo}")






class VersaoDAO:
   def __init__(self, host="localhost", user="root", password="ceub123456", database="db_auto"):
       # O construtor do DAO estabelece a conexão com o banco de dados
       try:
           self.conexao = mysql.connector.connect(
               host=host,
               user=user,
               password=password,
               database=database
           )
           self.cursor = self.conexao.cursor()
           print("Conexão com o banco de dados estabelecida com sucesso!")
       except mysql.connector.Error as err:
           print(f"Erro ao conectar ao banco de dados: {err}")
           self.conexao = None
           self.cursor = None


   def inserir(self, versao):
       # Insere um novo objeto Versao no banco de dados
       if not self.conexao:
           print("Erro: Nenhuma conexão com o banco de dados.")
           return


       sql = """
             INSERT INTO tb_versao (nme_versao, cod_modelo, vlr_modelo, img_modelo)
             VALUES (%s, %s, %s, %s)
             """
       valores = (versao.nme_versao, versao.cod_modelo, versao.vlr_modelo, versao.img_modelo)


       try:
           self.cursor.execute(sql, valores)
           self.conexao.commit()
           print(f"Versão '{versao.nme_versao}' inserida com sucesso!")
           versao.idt_versao = self.cursor.lastrowid
       except mysql.connector.Error as err:
           print(f"Erro ao inserir versão: {err}")
           self.conexao.rollback()


   def selecionar_tudo(self):
       # Seleciona todos os registros e os retorna como objetos Versao
       if not self.conexao:
           print("Erro: Nenhuma conexão com o banco de dados.")
           return []


       sql = "SELECT idt_versao, nme_versao, cod_modelo, vlr_modelo, img_modelo FROM tb_versao ORDER BY nme_versao"


       try:
           self.cursor.execute(sql)
           resultados = self.cursor.fetchall()


           lista_versoes = []
           for row in resultados:
               # Instancia Versao sem carregar o Modelo, usando o ID
               versao = Versao(
                   idt_versao=row[0],
                   nme_versao=row[1],
                   cod_modelo=row[2],
                   vlr_modelo=row[3],
                   img_modelo=row[4]
               )
               lista_versoes.append(versao)


           return lista_versoes
       except mysql.connector.Error as err:
           print(f"Erro ao selecionar versões: {err}")
           return []

   def selecionar_por_modelo(self, cod_modelo):
       # Seleciona todos os registros e os retorna como objetos Versao
       if not self.conexao:
           print("Erro: Nenhuma conexão com o banco de dados.")
           return []

       sql = "SELECT idt_versao, nme_versao, cod_modelo, vlr_modelo, img_modelo FROM tb_versao WHERE cod_modelo = %s ORDER BY nme_versao"

       try:
           self.cursor.execute(sql, [cod_modelo])
           resultados = self.cursor.fetchall()

           lista_versoes = []
           for row in resultados:
               # Instancia Versao sem carregar o Modelo, usando o ID
               versao = Versao(
                   idt_versao=row[0],
                   nme_versao=row[1],
                   cod_modelo=row[2],
                   vlr_modelo=row[3],
                   img_modelo=row[4]
               )
               lista_versoes.append(versao)

           return lista_versoes
       except mysql.connector.Error as err:
           print(f"Erro ao selecionar versões: {err}")
           return []

   def selecionar_por_idt(self, idt):
       # Seleciona uma versão por identificador
       if not self.conexao:
           print("Erro: Nenhuma conexão com o banco de dados.")
           return None


       sql = "SELECT idt_versao, nme_versao, cod_modelo, vlr_modelo, img_modelo FROM tb_versao WHERE idt_versao = %s"


       try:
           self.cursor.execute(sql, [idt])
           resultado = self.cursor.fetchone()
           if resultado is None:
               return None
           else:
               versao = Versao(
                   idt_versao=resultado[0],
                   nme_versao=resultado[1],
                   cod_modelo=resultado[2],
                   vlr_modelo=resultado[3],
                   img_modelo=resultado[4]
               )
               return versao


       except mysql.connector.Error as err:
           print(f"Erro ao selecionar versão: {err}")
           return None


   def atualizar(self, versao):
       # Atualiza um objeto Versao no banco de dados
       if not self.conexao:
           print("Erro: Nenhuma conexão com o banco de dados.")
           return


       sql = """
             UPDATE tb_versao
             SET nme_versao = %s,
                 cod_modelo = %s,
                 vlr_modelo = %s,
                 img_modelo = %s
             WHERE idt_versao = %s
             """
       valores = (versao.nme_versao, versao.cod_modelo, versao.vlr_modelo, versao.img_modelo, versao.idt_versao)


       try:
           self.cursor.execute(sql, valores)
           self.conexao.commit()
           print(f"Versão de ID {versao.idt_versao} atualizada com sucesso!")
       except mysql.connector.Error as err:
           print(f"Erro ao atualizar versão: {err}")
           self.conexao.rollback()


   def deletar(self, idt_versao):
       # Deleta uma versão pelo seu ID
       if not self.conexao:
           print("Erro: Nenhuma conexão com o banco de dados.")
           return


       sql = "DELETE FROM tb_versao WHERE idt_versao = %s"


       try:
           self.cursor.execute(sql, [idt_versao])
           self.conexao.commit()
           print(f"Versão de ID {idt_versao} deletada com sucesso!")
           return True
       except mysql.connector.Error as err:
           print(f"Erro ao deletar versão: {err}")
           self.conexao.rollback()
           return False


   def __dell__(self):
       # Método destrutor para fechar a conexão com o banco de dados
       if self.conexao and self.conexao.is_connected():
           self.cursor.close()
           self.conexao.close()
           print("Conexão com o banco de dados fechada.")