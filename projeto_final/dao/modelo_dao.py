import mysql.connector

from projeto_final.dao.versao_dao import VersaoDAO


# Classe que representa o objeto 'Modelo'
# Corresponde a uma linha da tabela tb_modelo
class Modelo:
   # O método construtor __init__ é chamado quando criamos um novo objeto Modelo.
   # Ele inicializa os atributos do objeto.
   def __init__(self, idt_modelo=None, nme_modelo='', cod_montadora=None):
       self.idt_modelo = idt_modelo
       self.nme_modelo = nme_modelo
       self.cod_montadora = cod_montadora
       self._montadora = None
       self._versoes = None


   @property
   def montadora(self):
       if self._montadora is None:
           from projeto_final.dao.montadora_dao import MontadoraDAO
           dao = MontadoraDAO()
           self._montadora = dao.selecionar_por_idt(self.cod_montadora)
       return self._montadora

   @property
   def versoes(self):
       if self._versoes is None:
           from projeto_final.dao.versao_dao import ModeloDAO
           dao = VersaoDAO()
           self._modelos = dao.selecionar_por_modelo(self.idt_modelo)
       return self._versoes




   # O método __str__ é útil para imprimir o objeto de forma amigável
   def __str__(self):
       return f"Id: {self.idt_modelo}, Nome: {self.nme_modelo}, Código Montadora: {self.cod_montadora}, Montadora: {self.montadora.nme_montadora}"




# Classe DAO (Data Access Object) para a tabela tb_modelo
# Responsável por todas as operações de banco de dados
class ModeloDAO:
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


   def inserir(self, modelo):
       # Método para inserir um novo objeto Modelo no banco de dados
       if not self.conexao:
           print("Erro: Nenhuma conexão com o banco de dados.")
           return


       sql = "INSERT INTO tb_modelo (nme_modelo, cod_montadora) VALUES (%s, %s)"
       valores = (modelo.nme_modelo, modelo.cod_montadora)


       try:
           self.cursor.execute(sql, valores)
           self.conexao.commit()
           print(f"Modelo '{modelo.nme_modelo}' inserida com sucesso!")
           # Atualiza o ID do objeto Modelo com o ID gerado pelo banco de dados
           modelo.idt_modelo = self.cursor.lastrowid
       except mysql.connector.Error as err:
           print(f"Erro ao inserir modelo: {err}")
           self.conexao.rollback()


   def selecionar_tudo(self):
       # Método para selecionar todos os registros e retorná-los como objetos Modelo
       if not self.conexao:
           print("Erro: Nenhuma conexão com o banco de dados.")
           return []


       sql = "SELECT idt_modelo, nme_modelo, cod_montadora FROM tb_modelo ORDER BY nme_modelo"


       try:
           self.cursor.execute(sql)
           resultados = self.cursor.fetchall()


           # Converte as tuplas do banco de dados em objetos Modelo
           lista_modelos = []
           for row in resultados:
               modelo = Modelo(idt_modelo=row[0], nme_modelo=row[1], cod_montadora=row[2])
               lista_modelos.append(modelo)


           return lista_modelos
       except mysql.connector.Error as err:
           print(f"Erro ao selecionar modelos: {err}")
           return []


   def selecionar_por_montadora(self, idt_montadora):
       # Método para selecionar todos os registros de uma montadora e retorná-los como objetos Modelo
       if not self.conexao:
           print("Erro: Nenhuma conexão com o banco de dados.")
           return []


       sql = "SELECT idt_modelo, nme_modelo, cod_montadora FROM tb_modelo WHERE cod_montadora = %s ORDER BY nme_modelo"


       try:
           self.cursor.execute(sql, [idt_montadora])
           resultados = self.cursor.fetchall()


           # Converte as tuplas do banco de dados em objetos Modelo
           lista_modelos = []
           for row in resultados:
               modelo = Modelo(idt_modelo=row[0], nme_modelo=row[1], cod_montadora=row[2])
               lista_modelos.append(modelo)


           return lista_modelos
       except mysql.connector.Error as err:
           print(f"Erro ao selecionar modelos: {err}")
           return []


   def selecionar_por_idt(self, idt):
       # Buscar um modelo por identificador
       if not self.conexao:
           print("Erro: Nenhuma conexão com o banco de dados.")
           return None


       sql = "SELECT idt_modelo, nme_modelo, cod_montadora FROM tb_modelo WHERE idt_modelo = %s"


       try:
           self.cursor.execute(sql, [idt])
           resultado = self.cursor.fetchone()
           if resultado is None:
               return None
           else:
               modelo = Modelo(idt_modelo=resultado[0], nme_modelo=resultado[1], cod_montadora=resultado[2])
               return modelo


       except mysql.connector.Error as err:
           print(f"Erro ao selecionar modelo: {err}")
           return []


   def atualizar(self, modelo):
       # Método para atualizar um objeto Modelo no banco de dados
       if not self.conexao:
           print("Erro: Nenhuma conexão com o banco de dados.")
           return


       sql = "UPDATE tb_modelo SET nme_modelo = %s, cod_montadora= %s WHERE idt_modelo = %s"
       valores = (modelo.nme_modelo, modelo.cod_montadora, modelo.idt_modelo)


       try:
           self.cursor.execute(sql, valores)
           self.conexao.commit()
           print(f"Modelo de ID {modelo.idt_modelo} atualizada com sucesso!")
       except mysql.connector.Error as err:
           print(f"Erro ao atualizar modelo: {err}")
           self.conexao.rollback()


   def deletar(self, idt_modelo):
       # Método para deletar uma modelo pelo seu ID
       if not self.conexao:
           print("Erro: Nenhuma conexão com o banco de dados.")
           return


       sql = "DELETE FROM tb_modelo WHERE idt_modelo = %s"


       try:
           self.cursor.execute(sql, [idt_modelo])
           self.conexao.commit()
           print(f"Modelo de ID {idt_modelo} deletada com sucesso!")
           return True
       except mysql.connector.Error as err:
           print(f"Erro ao deletar modelo: {err}")
           self.conexao.rollback()
           return False


   def __dell__(self):
       # Método destrutor para fechar a conexão com o banco de dados
       if self.conexao and self.conexao.is_connected():
           self.cursor.close()
           self.conexao.close()
           print("Conexão com o banco de dados fechada.")