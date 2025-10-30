import mysql.connector
from aula03a07.dao.montadora_dao import MontadoraDAO


# Classe que representa o objeto 'Modelo'
# Corresponde a uma linha da tabela tb_modelo
class Modelo:
    # O método construtor __init__ é chamado quando criamos um novo objeto Modelo.
    # Ele inicializa os atributos do objeto.
    def __init__(self, idt_modelo=None, nme_modelo='', cod_montadora=None, montadora=None):
        self.idt_modelo = idt_modelo
        self.nme_modelo = nme_modelo
        self.cod_montadora = cod_montadora
        self.montadora = montadora

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
            daoMontadora = MontadoraDAO()
            for row in resultados:
                montadora = daoMontadora.selecionar_por_idt(row[2])
                modelo = Modelo(idt_modelo=row[0], nme_modelo=row[1], cod_montadora=row[2], montadora=montadora)
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
                daoMontadora = MontadoraDAO()
                montadora = daoMontadora.selecionar_por_idt(resultado[2])
                modelo = Modelo(idt_modelo=resultado[0], nme_modelo=resultado[1], cod_montadora=resultado[2],
                                montadora=montadora)
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


# --- Smoke Test ---
if __name__ == "__main__":
    # 1. Cria uma instância do DAO, estabelecendo a conexão
    dao = ModeloDAO()

    if dao.conexao:
        # 2. Cria objetos Modelo (a lógica de negócios)
        modelo1 = Modelo(nme_modelo="Virtus", cod_montadora=2)
        modelo2 = Modelo(nme_modelo="Titano", cod_montadora=1)

        # 3. Usa o DAO para inserir os objetos no banco (a lógica de acesso a dados)
        dao.inserir(modelo1)
        dao.inserir(modelo2)

        # 4. Usa o DAO para selecionar todos os registros
        print("\nModelos cadastradas:")
        todas_modelos = dao.selecionar_tudo()
        for modelo in todas_modelos:
            print(modelo)
